import asyncio
import aiohttp
from bs4 import BeautifulSoup
import argparse
import logging
from logging.handlers import RotatingFileHandler
import json
from urllib.parse import urlparse, urljoin
import dns.resolver
import socket
from colorama import Fore, Style, init
import ssl
import OpenSSL
import re
import random
import aiodns
import subprocess
from tqdm import tqdm
import time
from functools import lru_cache

init(autoreset=True)

COMMON_SUBDIR = ['admin', 'login', 'wp-admin', 'wp-content', 'images', 'img', 'css', 'js', 'uploads', 'backup', 'api', 'dev', 'test', 'staging', 'beta', 'old', 'new', 'archive', 'mobile', 'forum', 'secure', 'private', 'public', 'internal', 'external', 'tools', 'services', 'apps', 'auth', 'portal', 'intranet', 'extranet', 'database', 'db', 'sql', 'ftp', 'sftp', 'ssh', 'mail', 'webmail', 'exchange', 'owa', 'cpanel', 'whm', 'hosting', 'cloud', 'cdn', 'assets', 'static', 'dynamic', 'temp', 'tmp', 'cache', 'logs', 'log', 'administrator', 'root', 'sys', 'system', 'wp', 'wordpress', 'joomla', 'drupal', 'magento', 'shop', 'store', 'cart', 'checkout', 'pay', 'payment', 'ssl']

COMMON_FILES = ['robots.txt', 'sitemap.xml', '.htaccess', 'crossdomain.xml', 'phpinfo.php', 'config.php', 'wp-config.php', '.env', '.git/HEAD', 'backup.sql', 'db.sql', 'dump.sql', 'database.sql', 'admin.php', 'login.php', 'wp-login.php', 'server-status', '.DS_Store', 'web.config', 'elmah.axd', 'trace.axd', 'backdoor.php', 'shell.php', 'c99.php', 'r57.php', 'webshell.php', 'config.inc.php', 'configuration.php', 'settings.php', 'info.php', 'test.php', 'phptest.php', 'php.ini', '.htpasswd', '.bash_history', '.ssh/id_rsa', 'id_rsa.pub', 'authorized_keys', 'access.log', 'error.log', 'server.log', 'www.log', 'backup.zip', 'backup.tar.gz', 'backup.rar', 'db_backup.sql', 'users.sql', 'passwords.txt', 'admin.txt', 'password.txt', 'web.log']

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

MAX_CONCURRENT_REQUESTS = 50

def setup_logging(log_level):
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    file_handler = RotatingFileHandler("cybersentry.log", maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

def print_banner():
    banner = f"""
{Fore.CYAN}
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗███╗   ██╗████████╗██████╗ ██╗   ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝ 
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝  
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗██║ ╚████║   ██║   ██║  ██║   ██║   
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   
{Style.RESET_ALL}
{Fore.YELLOW}╔═══════════════════════════════════════════════════════════════════════════╗
║  CyberSentry: Advanced Cybersecurity Intelligence Tool                      ║
║  Version: 1.0.0                                                             ║
║  Developed by: Luca Lorenzi for Orizon                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.RED}[!] CAUTION: Use responsibly and only with explicit permission.{Style.RESET_ALL}
"""
    print(banner)

async def fetch_url(session, url, semaphore, timeout=10):
    async with semaphore:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        try:
            async with session.get(url, timeout=timeout, allow_redirects=True, headers=headers) as response:
                return await response.text(), response.status
        except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
        return None, None

async def run_subfinder(domain):
    try:
        process = await asyncio.create_subprocess_exec(
            'subfinder', '-d', domain, '-silent',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stderr:
            logging.error(f"Subfinder error: {stderr.decode()}")
        return stdout.decode().splitlines()
    except Exception as e:
        logging.error(f"Error running subfinder: {str(e)}")
        return []

async def crawl_website(session, url, semaphore, max_depth=3, max_urls=100):
    visited = set()
    to_visit = [(url, 0)]
    found_urls = []

    while to_visit and len(found_urls) < max_urls:
        current_url, depth = to_visit.pop(0)
        if current_url in visited or depth > max_depth:
            continue

        visited.add(current_url)
        content, status = await fetch_url(session, current_url, semaphore)
        if content:
            found_urls.append(current_url)
            if depth < max_depth:
                soup = BeautifulSoup(content, 'html.parser')
                for a in soup.find_all('a', href=True):
                    next_url = urljoin(current_url, a['href'])
                    if next_url.startswith(url) and next_url not in visited:
                        to_visit.append((next_url, depth + 1))

    return found_urls

@lru_cache(maxsize=100)
def get_dns_records(domain):
    records = {}
    for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(rdata) for rdata in answers]
        except dns.resolver.NoAnswer:
            logging.info(f"No {record_type} record found for {domain}")
        except Exception as e:
            logging.warning(f"Error getting {record_type} records: {str(e)}")
    return records

@lru_cache(maxsize=100)
def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {"ip": ip}
    except Exception as e:
        logging.error(f"Error getting IP info: {str(e)}")
        return {}

@lru_cache(maxsize=100)
def get_ssl_info(domain):
    try:
        cert = ssl.get_server_certificate((domain, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        return {
            "subject": dict((k.decode(), v.decode()) for k, v in x509.get_subject().get_components()),
            "issuer": dict((k.decode(), v.decode()) for k, v in x509.get_issuer().get_components()),
            "version": x509.get_version(),
            "serial_number": x509.get_serial_number(),
            "not_before": x509.get_notBefore().decode(),
            "not_after": x509.get_notAfter().decode()
        }
    except Exception as e:
        logging.error(f"Error getting SSL info: {str(e)}")
        return {}

def extract_emails(text):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return list(set(re.findall(email_regex, text)))

def extract_phone_numbers(text):
    phone_regex = r'\b\+?[\d\s()-]{10,}\b'
    return list(set(re.findall(phone_regex, text)))

async def check_directory(session, url, semaphore):
    _, status = await fetch_url(session, url, semaphore, timeout=5)
    return url, status

async def check_file(session, url, semaphore):
    _, status = await fetch_url(session, url, semaphore, timeout=5)
    return url, status

async def scan_ports(ip):
    open_ports = []
    sem = asyncio.Semaphore(1000)  # Limit concurrent scans

    async def scan_port(port):
        async with sem:
            try:
                _, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=1)
                open_ports.append(port)
                writer.close()
                await writer.wait_closed()
            except:
                pass

    await asyncio.gather(*[scan_port(port) for port in COMMON_PORTS])
    return open_ports

async def analyze_domain(domain):
    url = f"https://{domain}"
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    async with aiohttp.ClientSession() as session:
        logging.info(f"Starting subdomain enumeration for {domain}")
        subdomains_task = asyncio.create_task(run_subfinder(domain))

        logging.info(f"Crawling website {url}")
        crawled_urls_task = asyncio.create_task(crawl_website(session, url, semaphore))

        logging.info("Checking for common directories and files")
        directories_task = asyncio.gather(*[check_directory(session, f"{url}/{subdir}", semaphore) for subdir in COMMON_SUBDIR])
        files_task = asyncio.gather(*[check_file(session, f"{url}/{file}", semaphore) for file in COMMON_FILES])

        logging.info("Retrieving DNS records")
        dns_records = get_dns_records(domain)

        logging.info("Getting IP information")
        ip_info = get_ip_info(domain)

        if ip_info.get('ip'):
            logging.info(f"Scanning ports for {ip_info['ip']}")
            open_ports_task = asyncio.create_task(scan_ports(ip_info['ip']))
        else:
            open_ports_task = asyncio.create_task(asyncio.sleep(0))

        logging.info("Retrieving SSL certificate information")
        ssl_info = get_ssl_info(domain)

        subdomains = await subdomains_task
        crawled_urls = await crawled_urls_task
        directories = await directories_task
        files = await files_task
        open_ports = await open_ports_task

        logging.info("Extracting emails and phone numbers")
        emails = set()
        phone_numbers = set()
        for link in crawled_urls:
            content, _ = await fetch_url(session, link, semaphore)
            if content:
                emails.update(extract_emails(content))
                phone_numbers.update(extract_phone_numbers(content))

    return {
        "domain": domain,
        "subdomains": subdomains,
        "crawled_urls": crawled_urls,
        "directories": [url for url, status in directories if status in [200, 301, 302, 403]],
        "files": [url for url, status in files if status in [200, 301, 302, 403]],
        "dns_records": dns_records,
        "ip_info": ip_info,
        "open_ports": open_ports,
        "ssl_info": ssl_info,
        "emails": list(emails),
        "phone_numbers": list(phone_numbers)
    }

def print_results(results):
    print(f"\n{Fore.GREEN}[*] CyberSentry Analysis Results for {results['domain']}:{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}[+] Basic Information:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}IP Address:{Style.RESET_ALL} {results['ip_info'].get('ip', 'N/A')}")
    print(f"  {Fore.YELLOW}Open Ports:{Style.RESET_ALL} {', '.join(map(str, sorted(results['open_ports'])))}")

    print(f"\n{Fore.CYAN}[+] Subdomains ({len(results['subdomains'])}):{Style.RESET_ALL}")
    for subdomain in results['subdomains'][:10]:
        print(f"  - {subdomain}")
    if len(results['subdomains']) > 10:
        print(f"  ... and {len(results['subdomains']) - 10} more")

    print(f"\n{Fore.CYAN}[+] Directories ({len(results['directories'])}):{Style.RESET_ALL}")
    for directory in results['directories'][:10]:
        print(f"  - {directory}")
    if len(results['directories']) > 10:
        print(f"  ... and {len(results['directories']) - 10} more")

    print(f"\n{Fore.CYAN}[+] Sensitive Files ({len(results['files'])}):{Style.RESET_ALL}")
    for file in results['files'][:10]:
        print(f"  - {file}")
    if len(results['files']) > 10:
        print(f"  ... and {len(results['files']) - 10} more")

    print(f"\n{Fore.CYAN}[+] DNS Records:{Style.RESET_ALL}")
    for record_type, records in results['dns_records'].items():
        print(f"  {Fore.YELLOW}{record_type}:{Style.RESET_ALL}")
        for record in records[:5]:
            print(f"    - {record}")
        if len(records) > 5:
            print(f"    ... and {len(records) - 5} more")

    print(f"\n{Fore.CYAN}[+] SSL Certificate Information:{Style.RESET_ALL}")
    ssl_info = results['ssl_info']
    print(f"  {Fore.YELLOW}Subject:{Style.RESET_ALL} {ssl_info.get('subject', {}).get('CN', 'N/A')}")
    print(f"  {Fore.YELLOW}Issuer:{Style.RESET_ALL} {ssl_info.get('issuer', {}).get('CN', 'N/A')}")
    print(f"  {Fore.YELLOW}Valid From:{Style.RESET_ALL} {ssl_info.get('not_before', 'N/A')}")
    print(f"  {Fore.YELLOW}Valid To:{Style.RESET_ALL} {ssl_info.get('not_after', 'N/A')}")

    print(f"\n{Fore.CYAN}[+] Emails Found ({len(results['emails'])}):{Style.RESET_ALL}")
    for email in results['emails'][:10]:
        print(f"  - {email}")
    if len(results['emails']) > 10:
        print(f"  ... and {len(results['emails']) - 10} more")

    print(f"\n{Fore.CYAN}[+] Phone Numbers Found ({len(results['phone_numbers'])}):{Style.RESET_ALL}")
    for phone in results['phone_numbers'][:10]:
        print(f"  - {phone}")
    if len(results['phone_numbers']) > 10:
        print(f"  ... and {len(results['phone_numbers']) - 10} more")

    print(f"\n{Fore.CYAN}[+] Crawled URLs ({len(results['crawled_urls'])}):{Style.RESET_ALL}")
    for url in results['crawled_urls'][:10]:
        print(f"  - {url}")
    if len(results['crawled_urls']) > 10:
        print(f"  ... and {len(results['crawled_urls']) - 10} more")

async def main(args):
    print_banner()
    setup_logging(args.log_level)
    logging.info(f"Starting CyberSentry analysis for domain: {args.domain}")

    start_time = time.time()
    results = await analyze_domain(args.domain)
    end_time = time.time()

    print_results(results)

    output_file = f"{args.domain}_cybersentry_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    logging.info(f"Detailed results saved to {output_file}")
    logging.info(f"Total execution time: {end_time - start_time:.2f} seconds")

def run():
    parser = argparse.ArgumentParser(description="CyberSentry: Advanced Cybersecurity Intelligence Tool")
    parser.add_argument("domain", help="Target domain to analyze")
    parser.add_argument("--log-level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO', help="Set the logging level")
    args = parser.parse_args()

    asyncio.run(main(args))

if __name__ == '__main__':
    run()
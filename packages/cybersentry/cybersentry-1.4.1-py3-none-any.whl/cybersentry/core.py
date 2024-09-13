import asyncio
import aiohttp
from bs4 import BeautifulSoup
import argparse
import json
import csv
from urllib.parse import urlparse, urljoin
import dns.resolver
import socket
from colorama import Fore, Style, init
import ssl
import OpenSSL
import re
import random
import aiodns
from tqdm import tqdm
import time
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

init(autoreset=True)

MAX_CONCURRENT_REQUESTS = 50

COMMON_SUBDIR = ['admin', 'login', 'wp-admin', 'wp-content', 'images', 'img', 'css', 'js', 'uploads', 'backup', 'api', 'dev', 'test', 'staging', 'beta', 'old', 'new', 'archive', 'mobile', 'forum', 'secure', 'private', 'public', 'internal', 'external', 'tools', 'services', 'apps', 'auth', 'portal', 'intranet', 'extranet', 'database', 'db', 'sql', 'ftp', 'sftp', 'ssh', 'mail', 'webmail', 'exchange', 'owa', 'cpanel', 'whm', 'hosting', 'cloud', 'cdn', 'assets', 'static', 'dynamic', 'temp', 'tmp', 'cache', 'logs', 'log', 'administrator', 'root', 'sys', 'system', 'wp', 'wordpress', 'joomla', 'drupal', 'magento', 'shop', 'store', 'cart', 'checkout', 'pay', 'payment', 'ssl']

COMMON_FILES = ['robots.txt', 'sitemap.xml', '.htaccess', 'crossdomain.xml', 'phpinfo.php', 'config.php', 'wp-config.php', '.env', '.git/HEAD', 'backup.sql', 'db.sql', 'dump.sql', 'database.sql', 'admin.php', 'login.php', 'wp-login.php', 'server-status', '.DS_Store', 'web.config', 'elmah.axd', 'trace.axd', 'backdoor.php', 'shell.php', 'c99.php', 'r57.php', 'webshell.php', 'config.inc.php', 'configuration.php', 'settings.php', 'info.php', 'test.php', 'phptest.php', 'php.ini', '.htpasswd', '.bash_history', '.ssh/id_rsa', 'id_rsa.pub', 'authorized_keys', 'access.log', 'error.log', 'server.log', 'www.log', 'backup.zip', 'backup.tar.gz', 'backup.rar', 'db_backup.sql', 'users.sql', 'passwords.txt', 'admin.txt', 'password.txt', 'web.log']

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def print_banner():
    banner = f"""
{Fore.GREEN}
   ______      __              _____            __            
  / ____/_  __/ /_  ___  _____/ ___/___  ____  / /________  __
 / /   / / / / __ \/ _ \/ ___/\__ \/ _ \/ __ \/ __/ ___/ / / /
/ /___/ /_/ / /_/ /  __/ /   ___/ /  __/ / / / /_/ /  / /_/ / 
\____/\__, /_.___/\___/_/   /____/\___/_/ /_/\__/_/   \__, /  
     /____/                                          /____/   
{Style.RESET_ALL}
{Fore.CYAN}[+] Advanced Cybersecurity Intelligence Tool{Style.RESET_ALL}
{Fore.YELLOW}[!] Use responsibly and only with explicit permission{Style.RESET_ALL}
    """
    print(banner)

async def fetch_url(session, url, semaphore, timeout=10):
    async with semaphore:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        try:
            async with session.get(url, timeout=timeout, allow_redirects=True, headers=headers) as response:
                return await response.text(), response.status
        except Exception as e:
            return None, None

async def enumerate_subdomains(domain, session):
    subdomains = set()

    async def bevigil_enum():
        api_key = os.getenv('BEVIGIL_API_KEY')
        if not api_key:
            return set()
        url = f"https://osint.bevigil.com/api/{domain}/subdomains/"
        headers = {"X-Access-Token": api_key}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return set(data.get('subdomains', []))
            else:
                return set()

    async def crtsh_enum():
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return set(item['name_value'] for item in data)
            else:
                return set()

    async def virustotal_enum():
        api_key = os.getenv('VIRUSTOTAL_API_KEY')
        if not api_key:
            return set()
        url = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains"
        headers = {"x-apikey": api_key}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return set(item['id'] for item in data.get('data', []))
            else:
                return set()

    tasks = [
        bevigil_enum(),
        crtsh_enum(),
        virustotal_enum(),
    ]

    results = await asyncio.gather(*tasks)
    for result in results:
        subdomains.update(result)

    return list(subdomains)

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

async def check_directory(session, url, semaphore):
    _, status = await fetch_url(session, url, semaphore, timeout=5)
    return url, status

async def check_file(session, url, semaphore):
    _, status = await fetch_url(session, url, semaphore, timeout=5)
    return url, status

@lru_cache(maxsize=100)
def get_dns_records(domain):
    records = {}
    for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(rdata) for rdata in answers]
        except dns.resolver.NoAnswer:
            pass
        except Exception as e:
            pass
    return records

@lru_cache(maxsize=100)
def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {"ip": ip}
    except Exception as e:
        return {}

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
        return {}

async def analyze_domain(domain, progress_bar):
    url = f"https://{domain}"
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    async with aiohttp.ClientSession() as session:
        progress_bar.update(5)
        subdomains = await enumerate_subdomains(domain, session)
        progress_bar.update(20)

        crawled_urls = await crawl_website(session, url, semaphore)
        progress_bar.update(20)

        directories = [url for url, status in await asyncio.gather(*[check_directory(session, f"{url}/{subdir}", semaphore) for subdir in COMMON_SUBDIR]) if status in [200, 301, 302, 403]]
        progress_bar.update(15)

        files = [url for url, status in await asyncio.gather(*[check_file(session, f"{url}/{file}", semaphore) for file in COMMON_FILES]) if status in [200, 301, 302, 403]]
        progress_bar.update(15)

        dns_records = get_dns_records(domain)
        progress_bar.update(5)

        ip_info = get_ip_info(domain)
        progress_bar.update(5)

        if ip_info.get('ip'):
            open_ports = await scan_ports(ip_info['ip'])
        else:
            open_ports = []
        progress_bar.update(10)

        ssl_info = get_ssl_info(domain)
        progress_bar.update(5)

    return {
        "domain": domain,
        "subdomains": subdomains,
        "crawled_urls": crawled_urls,
        "directories": directories,
        "files": files,
        "dns_records": dns_records,
        "ip_info": ip_info,
        "open_ports": open_ports,
        "ssl_info": ssl_info,
    }

async def main(args):
    print_banner()
    domain = args.domain
    
    with tqdm(total=100, bar_format="{l_bar}{bar}") as progress_bar:
        progress_bar.set_description("Analyzing domain")
        results = await analyze_domain(domain, progress_bar)

    print(f"\n{Fore.GREEN}[+] Analysis complete!{Style.RESET_ALL}")
    
    output_json = f"{domain}_cybersentry_results.json"
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"{Fore.CYAN}[*] JSON results saved to: {output_json}{Style.RESET_ALL}")

    output_csv = f"{domain}_cybersentry_results.csv"
    with open(output_csv, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Data"])
        for key, value in results.items():
            if isinstance(value, list):
                for item in value:
                    writer.writerow([key, item])
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    writer.writerow([f"{key}.{sub_key}", sub_value])
            else:
                writer.writerow([key, value])
    print(f"{Fore.CYAN}[*] CSV results saved to: {output_csv}{Style.RESET_ALL}")

def run():
    parser = argparse.ArgumentParser(description="CyberSentry: Advanced Cybersecurity Intelligence Tool")
    parser.add_argument("domain", help="Target domain to analyze")
    args = parser.parse_args()

    asyncio.run(main(args))

if __name__ == '__main__':
    run()
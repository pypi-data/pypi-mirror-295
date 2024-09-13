# CyberSentry

CyberSentry is an Advanced Cybersecurity Intelligence Tool designed for comprehensive domain analysis and threat assessment.

## Installation

1. Ensure you have Python 3.6 or later installed.

2. It's recommended to use a virtual environment:

```bash
python -m venv cybersentry-env
source cybersentry-env/bin/activate  # On Windows use `cybersentry-env\Scripts\activate`
```

3. Install CyberSentry:

```bash
pip install cybersentry
```

If you're installing from the source:

```bash
git clone https://github.com/Lxsanto/cybersentry.git
cd cybersentry
pip install -e .
```

This will install CyberSentry and all its dependencies.

## Usage

```bash
cybersentry example.com
```

## Key Features

- Intelligent Subdomain Discovery
- Deep Web Crawling and Analysis
- Sensitive Directory and File Detection
- Comprehensive DNS Record Analysis
- Advanced IP Intelligence Gathering
- Strategic Port Vulnerability Scanning
- In-depth SSL Certificate Verification
- Automated Email and Phone Number Extraction
- Progress Bar for Real-time Analysis Updates
- JSON and CSV Output

## Configuration

Some features require API keys. Create a `.env` file in the project root with the following content:

```
BEVIGIL_API_KEY=your_bevigil_api_key
VIRUSTOTAL_API_KEY=your_virustotal_api_key
# Add other API keys as needed
```

## Security Notice

CyberSentry is a powerful tool intended for authorized security professionals and ethical hackers. Always obtain explicit permission before analyzing any domain or network you do not own or have the right to test.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Troubleshooting

If you encounter any issues with missing dependencies, try updating pip and reinstalling:

```bash
pip install --upgrade pip
pip install --upgrade cybersentry
```

If problems persist, please open an issue on the GitHub repository.

## Authors

* **Luca Lorenzi** - *Initial work* - [Lxsanto](https://github.com/Lxsanto)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
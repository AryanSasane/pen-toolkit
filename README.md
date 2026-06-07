# Penetration Testing Toolkit

A modular web application penetration testing toolkit. Built to work alongside the [Web Attack Analyzer](https://github.com/AryanSasane/web-attack-analyzer) — attacks performed with this toolkit can be captured and detected by the analyzer, closing the full attack-defense loop.

## Modules
- **SQLi Tester** — detects SQL injection using error-based and response size analysis
- **Directory Fuzzer** — discovers hidden paths and endpoints using wordlists
- **Brute Force** — tests login forms for weak credentials

## Usage

### Run all modules
```bash
python main.py --target http://localhost --all
```

### Run individually
```bash
python main.py --target http://localhost --sqli
python main.py --target http://localhost --fuzz
python main.py --target http://localhost --brute
```

### Custom report
```bash
python main.py --target http://localhost --all --report findings.json
```

## Full Attack-Defense Loop
pen-toolkit attacks target
↓
tcpdump captures traffic
↓
web-attack-analyzer detects attacks
↓
dashboard displays live alerts

## Installation
```bash
git clone https://github.com/AryanSasane/pen-toolkit.git
cd pen-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Lab Setup
This toolkit is designed to be used against [DVWA](https://github.com/digininja/DVWA) running in Docker:
```bash
sudo docker run -d -p 80:80 --name dvwa vulnerables/web-dvwa
```

## Tech Stack
Python, Requests, Colorama

## ⚠️ Legal Notice
This tool is for educational purposes only. Only use against systems you own or have explicit written permission to test.
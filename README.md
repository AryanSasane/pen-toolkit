# Penetration Testing ToolKit

A modular penetration testing toolkit targeting web applications. Built to work alongside the Web Analyzer Project in order to test its capabilities.

## Modules 
- **SQLi Tester** - detects SQL Injection vulnerabilities
- **Directory Fuzzer** - discovers hidden paths and endpoints
- **Brute Force** - tests login forms for weak credentials

## Usage
```bash
# Run all modules
python main.py --target http://localhost --all

#Run individually
python main.py --target http://localhost --sqli
python main.py --target http://localhost --fuzz
python main.py --target http://localhost --brute
```

## Stack
Python, Requests, Colorama
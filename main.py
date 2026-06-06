import argparse
import requests
from utils.reporter import save_report, print_summary

def get_session(base_url: str, username: str, password: str):
    session = requests.Session()
    login_url = f"{base_url}/login.php"

    response = session.get(login_url)
    token = None

    if "user_token" in response.text:
        import re
        match = re.search(r"user_token'\s*value='([^']+)'", response.text)
        if match:
            token = match.group(1)

    data = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": token or ""
    }
    session.post(login_url, data=data)
    print(f"[*] Logged in as {username}")
    return session

def main():
    parser = argparse.ArgumentParser(description="Penetration Testing ToolKit")
    parser.add_argument("--target",         required=True, help="Base URL of target")
    parser.add_argument("--username",       default="admin", help="Login username")
    parser.add_argument("--password",       default="password", help="Login password")
    parser.add_argument("--sqli",           action="store_true", help="Run SQL Injection tester")
    parser.add_argument("--fuzz",           action="store_true", help="Run directory fuzzer")
    parser.add_argument("--brute",          action="store_true", help="Run brute force module")
    parser.add_argument("--all",            action="store_true", help="Run all modules")
    parser.add_argument("--report",         default="report.json", help="Output report path")
    args = parser.parse_args()

    print(f"\n[*] Target: {args.target}")
    print(f"[*] Starting penetration test...\n")

    session = get_session(args.target, args.username, args.password)
    findings = {"target": args.target}

    if args.sqli or args.all:
        from modules.sqli_tester import test_sqli
        sqli_url = f"{args.target}/vulnerabilities/sqli/"
        findings["sqli"] = test_sqli(sqli_url, "id", session=session)

    if args.fuzz or args.all:
        from modules.dir_fuzzer import fuzz_dirs
        findings["fuzzer"] = fuzz_dirs(args.target, "wordlists/common_dirs.txt", session=session)
    
    if args.brute or args.all:
        from modules.brute_force import brute_force
        brute_url = f"{args.target}/vulnerabilities/brute/"
        brute_session = get_session(args.target, args.username, args.password)
        result = brute_force(brute_url, args.username, "wordlists/common_passwords.txt", session=brute_session)
        findings["brute_force"] = [result] if result else []

    print_summary(findings)
    save_report(findings, args.report)

if __name__ == "__main__":
    main() 
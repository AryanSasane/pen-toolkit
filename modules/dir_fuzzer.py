import requests
import colorama
from colorama import Fore, Style

colorama.init()

def load_wordlist(path: str) -> list:
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def fuzz_dirs(base_url: str, wordlist_path: str, session=None) -> list:
    findings = []
    requester = session or requests
    wordlist = load_wordlist(wordlist_path)

    print(f"\n[*] Fuzzing {base_url} with {len(wordlist)} paths...")

    for path in wordlist:
        url = f"{base_url}/{path}"
        try:
            response = requester.get(url, allow_redirects=False)
            status = response.status_code

            if status == 200:
                findings.append({"path": url, "status": status})
                print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL} {url} - {status}")
            elif status == 301 or status == 302:
                findings.append({"path": url, "status": status})
                print(f"{Fore.YELLOW}[REDIRECT]{Style.RESET_ALL} {url} - {status}")
            elif status == 403:
                findings.append({"path": url, "status": status})
                print(f"{Fore.YELLOW}[FORBIDDEN]{Style.RESET_ALL} {url} - {status}")
            else:
                print(f"{Fore.RED}[NOT FOUND]{Style.RESET_ALL} {url} - {status}")
        
        except requests.exceptions.RequestException as e:
            print(f"{Fore.YELLOW}[ERROR]{Style.RESET_ALL} {e}") 
    
    return findings
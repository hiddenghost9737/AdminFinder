import requests
from colorama import Fore, Style
import concurrent.futures

print(Fore.GREEN+Style.BRIGHT+'''

****************************************************
*                 Admin Finder Script               *
****************************************************
*  Find potential admin panel URLs for a given base  *
*               URL using a list of patterns.        *
****************************************************
*                    Usage Example:                 *
*     python adminfinder.py                          *
****************************************************

''')

def get_status_code(url, session):
    try:
        response = session.head(url, allow_redirects=True, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException:
        return None

def check_admin_url(base_url, admin_url, session):
    try:
        full_url = f"{base_url.rstrip('/')}/{admin_url.lstrip('/')}"
        parsed_url = requests.utils.urlparse(full_url)
        if not parsed_url.scheme:
            full_url = f"[+]https://{full_url}"
        status_code = get_status_code(full_url, session)
        return full_url, status_code
    except Exception:
        return None, None

def print_colored_url(url, status_code):
    if status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[+]{url} - {status_code}{Style.RESET_ALL}")
        return url
    elif status_code == 404:
        print(f"{Fore.RED+Style.BRIGHT}[-]{url} - {status_code} (Not Found){Style.RESET_ALL}")
    else:
        print(f"{url} - Unable to fetch status code")

def main():
    base_url = input(Fore.BLUE+Style.BRIGHT+"[+] Enter the base URL to scrape: ")

    try:
        # Check if the base URL is valid
        requests.get(base_url, timeout=5)
    except requests.exceptions.RequestException:
        print(Fore.RED+Style.BRIGHT+f"[+]Error: Unable to establish a connection with the base URL {base_url}. Please check the URL.[+]")
        return

    admin_file_path = input(Fore.BLUE+Style.BRIGHT+"[+]Enter the path to admin patterns file (e.g., admin.txt): ")

    try:
        with open(admin_file_path, 'r') as admin_file:
            admin_patterns = [line.strip() for line in admin_file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Admin patterns file not found at {admin_file_path}")
        return
    except Exception as e:
        print(f"Error reading admin patterns file: {e}")
        return

    print(Fore.WHITE+Style.BRIGHT+f"[+] Base URL: {base_url}")
    print(f"[+] Checking URLs from {admin_file_path}:")

    found_urls = []

    with requests.Session() as session, concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_admin_url, base_url, admin_pattern, session): admin_pattern for admin_pattern in admin_patterns}

        for future in concurrent.futures.as_completed(future_to_url):
            admin_pattern = future_to_url[future]
            try:
                full_url, status_code = future.result()
                if full_url is not None:
                    success_url = print_colored_url(full_url, status_code)
                    if success_url:
                        found_urls.append(success_url)
            except Exception as e:
                print(f"Error processing {admin_pattern}: {e}")

    # Save found URLs to success.txt
    with open('success.txt', 'w') as success_file:
        for url in found_urls:
            success_file.write(f"{url}\n")

    print(Fore.YELLOW+Style.BRIGHT+f"Found URLs saved to success.txt")

if __name__ == "__main__":
    main()

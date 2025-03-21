import requests

target = input("Enter domain: ")
url = f"https://crt.sh/?q={target}&output=json"

print("[*] Fetching subdomains...")
response = requests.get(url).json()

subdomains = set(entry['name_value'] for entry in response)

for subdomain in subdomains:
    print(subdomain)

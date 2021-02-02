import requests
import re
from datetime import datetime
import json

link = "https://www.instagram.com/"
link_login = "https://www.instagram.com/accounts/login/ajax/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
hal_depan = requests.get(link,headers=headers)

# print(hal_depan.content)

with open('index.html','w') as file:
    file.write(hal_depan.text)
csrf = re.findall(r'{"config":{"csrf_token":"(.*)","viewer"',hal_depan.text)[0]
print(csrf)

username = 'user_instagram_anda'
password = 'pass_instagramanda'
time = int(datetime.now().timestamp())

payload = {
    'username': username,
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
    'queryParams': {},
    'optIntoOneTap': 'false'
}

login_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
    "x-csrftoken": csrf
}

login = requests.post(link_login,data=payload,headers=login_header)
# print(login.content)

json_response = json.loads(login.content)
print(json_response)

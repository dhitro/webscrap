import requests
import re
from datetime import datetime
import json
from typing import BinaryIO


link = "https://www.instagram.com/"
link_login = "https://www.instagram.com/accounts/login/ajax/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
hal_depan = requests.get(link,headers=headers)

# print(hal_depan.content)

with open('index.html','w') as file:
    file.write(hal_depan.text)
csrf = re.findall(r'{"config":{"csrf_token":"(.*)","viewer"',hal_depan.text)[0]
print(csrf)

username = 'testting50'
password = 'bisangoding'
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
# print(json_response)
def getbinary(photo:BinaryIO):
    return photo

if json_response['authenticated']==True:
    print("Anda Berhasil Login")
    cookies_login = login.cookies
    cookie_jar = cookies_login.get_dict()
    print(cookie_jar)

    session_login = {
        "csrf_token": cookie_jar['csrftoken'],
        "session_id": cookie_jar['sessionid']
    }

    cookies = {
        "sessionid": session_login['session_id'],
        "csrftoken": session_login['csrf_token']
    }

    #upload image
    with open('1.jpg','rb') as image:
        testimage = getbinary(image)
        headers_postphoto = {
            "content-type": "image / jpg",
            "content-length": "1",
            "X-Entity-Name": f"fb_uploader_{time}",
            "Offset": "0",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/77.0.3865.120 Safari/537.36",
            "x-entity-length": "1",
            "X-Instagram-Rupload-Params": f'{{"media_type": 1, "upload_id": {time}, "upload_media_height": 1080,'
                                          f' "upload_media_width": 1080}}',
            "x-csrftoken": session_login['csrf_token'],
            # "x-ig-app-id": "1217981644879628",
        }

        upload_photo = requests.post(f'https://www.instagram.com/rupload_igphoto/fb_uploader_{time}',
                                     data=testimage,headers=headers_postphoto,cookies=cookies)
        json_upload = json.loads(upload_photo.text)

        print(json_upload)
        # get id upload
        upload_id = json_upload['upload_id']
        # insert text nya caption gambar

        # url = 'https://www.instagram.com/create/configure/'
        # url = 'https://www.instagram.com/create/configure/'
        url_story = 'https://www.instagram.com/create/configure_to_story/'

        caption = 'Pagi Ini Ngoding Sambil Ketawa Ketiwi'
        payload_caption = f'upload_id={upload_id}&caption={caption}&usertags=&custom_accessibility_caption=&retry_timeout='

        header_caption = {
            'authority': 'www.instagram.com',
            # 'x-ig-www-claim': 'hmac.AR2-43UfYbG2ZZLxh-BQ8N0rqGa-hESkcmxat2RqMAXejXE3',
            # 'x-instagram-ajax': 'adb961e446b7-hot',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/85.0.4183.121 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-csrftoken': session_login['csrf_token'],
            # 'x-ig-app-id': '1217981644879628',
            'origin': 'https://www.instagram.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.instagram.com/create/details/',
            'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
        }

        # posting_caption = requests.post(url,headers=header_caption,data=payload_caption,cookies=cookies)
        posting_story = requests.post(url_story, headers=header_caption, data=payload_caption, cookies=cookies)

        # json_caption = json.loads(posting_caption.text)
        # print(json_caption)
        print(posting_caption.text)



else:
    print("Anda gagal login")
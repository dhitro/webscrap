from bs4 import BeautifulSoup
import requests
import time
import re
import json
from pathlib import Path

def bacamanga():
    URL_HOME = 'https://mangapark.net'
    html = requests.get(URL_HOME).text
    # print(html)
    soup = BeautifulSoup(html, 'lxml')
    isimanga = soup.find_all('div', class_='item')
    # print(isimanga)
    for manga in isimanga:
        judul = manga.a['title']
        filter = 'The Peerless Sword God'
        if filter in judul:
            chapter = manga.find_all('a', class_="visited")
            # print(judul)
            ch = ''
            for chp in chapter:
                ch += chp.text + ' '
                URL_HREF = chp['href']
                #URL_PAGE = f'{URL_HOME}{URL_HREF}'
                URL_PAGE = '{}{}'.format(URL_HOME,URL_HREF)
                # print(URL_PAGE)
                page = requests.get(URL_PAGE).text
                total_page = re.findall(r'var t_a_c =(.*);',page)[0]
                # print(total_page)
                total_page = int(total_page)
                Path(chp.text).mkdir(parents=True, exist_ok=True)

                for ipage in range(total_page):
                    pagetujuan = ipage + 1
                    # print(pagetujuan)
                    URL_HALAMAN = URL_PAGE[0:-1:]
                    # print(f'{URL_HALAMAN}{pagetujuan}')
                    page_halaman = requests.get(f'{URL_HALAMAN}{pagetujuan}').text
                    # cari Image
                    json_image = re.findall(r'var _load_pages =(.*);',page_halaman)[0]
                    #print(json_image)
                    json_load = json.loads(json_image)
                    for ijson in json_load:
                        URL_IMAGE = ijson['u']
                        # print(URL_IMAGE)
                        myimage = Path(f'{chp.text}/{pagetujuan}.jpg')
                        if myimage.is_file():
                            print(f'File {chp.text}/{pagetujuan}.jpg  Sudah Ada ')
                        else:
                            downloaded_image = requests.get(URL_IMAGE)
                            open(f'{chp.text}/{pagetujuan}.jpg','wb').write(downloaded_image.content)
                            print(f'Image {pagetujuan}.jpg Berhasil Di Download')


if __name__ == '__main__':
    while True:
        menit = 20
        print(f'apps berjalan dalam waktu periodik {menit} menit')
        bacamanga()
        time.sleep(menit * 60)
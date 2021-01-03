from bs4 import BeautifulSoup
import requests
import time
# with open('index.html','r') as html_data:
#     content = html_data.read()
#     # print(content)
#     soup = BeautifulSoup(content,'lxml')
#     cari_div = soup.find_all('div', class_="row-course")
#     for child in cari_div:
#         title = child.h2.text
#         harga = child.h3.span.text
#         print(f"title : {title} price: {harga}")

def bacamanga():
    html = requests.get('https://mangapark.net/').text
    #print(html)
    soup = BeautifulSoup(html,'lxml')
    isimanga = soup.find_all('div',class_='item')
    #print(isimanga)
    for manga in isimanga:
        judul = manga.a['title']
        filter = 'Dr. Stone'
        if filter in judul:
            chapter = manga.find_all('a',class_="visited")
            #print(judul)
            ch = ''
            for chp in chapter:
                ch += chp.text+' '
            #print(ch)
            update = manga.find_all('i')[1].text
            # print(update)
            with open('mangapark.txt','a') as ff:
                ff.write(f"{judul} : Chapter {ch} updated {update} \n")
    print('File Berhasil Dibuat')

if __name__ == '__main__':
    while True:
        menit = 20
        print(f'apps berjalan dalam waktu periodik {menit} menit')
        bacamanga()
        time.sleep(menit*60)

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

directory= os.getcwd()
if not os.path.exists(f'{directory}/images/'):
    os.mkdir(f'{directory}/images/')
user_agent = UserAgent().random
header = {'user-agent': user_agent}
home_page = 'https://zastavok.net/'
response = requests.get(home_page, headers=header)
print(response.status_code)

soup = BeautifulSoup(response.text, 'lxml')

all_pages = int(soup.find('div', id='clsLink3').contents[-3].text)

for page_number in range(1, all_pages):
    response = requests.get(f'{home_page}/{page_number}', headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    block_foto = soup.find('div', class_='block-photo')
    foto_links = [i['href'] for i in block_foto.find_all('a', itemprop='url')]
    for link in foto_links:
        response = requests.get(f'{home_page}{link}', headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
        img_link = soup.find('img', id='target')['src']
        user_agent = UserAgent().random
        header = {'user-agent': user_agent}
        image_bytes = requests.get(f'{home_page}{img_link}', headers=header).content
        name_img = img_link[img_link.rindex('/')+1:]
        with open(f'images/{name_img}', 'wb') as file:
            file.write(image_bytes)
            print(f'Сохранен файл: {name_img}')
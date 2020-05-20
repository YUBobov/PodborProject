import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Pool, Lock
import time
import os
from django.core.management.base import BaseCommand
import django
django.setup()

from webexample.models import FTTx
from webexample.models import ADSS
from webexample.models import Tip8
from webexample.models import Vkanal
from webexample.models import Vgrunt
from webexample.models import Raspredelitelnyj
from webexample.models import Ognestojkij
from webexample.models import Universalnyj


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
           'accept': '*/*'}
HOST = 'https://shop.nag.ru'


#получение страницы для парсинга
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

#получение данных со страницы
def get_content(html, volokno, kN=None):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='col-lg-3 col-lm-4 col-md-6 col-sm-12 col-xxl-25')
    cabel = []
    if kN:
        kN = kN
    else:
        kN = 0
    for item in items:
        if item.find('div', class_='sale'):
            price = item.find('div', class_='sale').get_text(strip=True).replace('\xa0', '').replace('От ','')
        else:
            price = 0
        cabel.append({
            'name': item.find('div', class_='product-name slideup').get_text().replace('  file_copy ', ''),
            'link': HOST + item.find('a', class_='cut-clamp').get('href'),
            'price': price,
            'volokna': volokno,
            'kN': kN
        })
    return cabel

#получаем количество страниц
def get_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('ul', class_='flat-pagination style1')
    if pages:
        for page in pages:
            page = page.find_all('li')[-2].get_text(strip=True)
            return int(page)
    else:
        return 1

#получаем значение кН
def get_kN(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('ul', class_='box-checkbox')
    items = items[2].find_all('li', class_='check-box')
    kN = []
    for item in items:
        a = item.get_text(strip=True).split(' ')
        kN.append(a[0])
    return kN


# получаем список волокн
def get_volokno(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('ul', class_='box-checkbox')
    items = items[1].find_all('li', class_='check-box')
    volokno = []
    for item in items:
        a = item.get_text(strip=True).split(' ')
        volokno.append(a[0])
    return volokno


#парсинг
def parse_FTTx(lock):
    cabel_FTTx = []
    html = get_html('https://shop.nag.ru/catalog/01919.opticheskij-kabel/08679.fttx')
    volokn = get_volokno(html.text)
    print(volokn)
    for volokno in volokn:
        html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/08679.fttx?count=20&default_view=2&filter_147_{volokno}=true&in_stock=&page=1&sort=popularity_desc')
        if html.status_code == 200:
            page_count = get_page(html.text)
            for page in range(1, page_count+1):
                print(f'Идет парсинг страницы {page} из {page_count}')
                html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/08679.fttx?count=20&default_view=2&filter_147_{volokno}=true&in_stock=&page=1&sort=popularity_desc', params= {'page': page})
                cabel_FTTx.extend(get_content(html.text, volokno))
        else:
            print('Error')
    lock.acquire()
    for i in range(0, len(cabel_FTTx)):
       try:
           fttx = FTTx.objects.get(link = cabel_FTTx[i]['link'])
           fttx.name = cabel_FTTx[i]['name']
           fttx.volokno = int(cabel_FTTx[i]['volokna'])
           fttx.kN = cabel_FTTx[i]['kN']
           fttx.price = int(cabel_FTTx[i]['price'])
           fttx.save()
       except FTTx.DoesNotExist:
           fttx = FTTx(
                name = cabel_FTTx[i]['name'],
                volokno = int(cabel_FTTx[i]['volokna']),
                kN = cabel_FTTx[i]['kN'],
                price = int(cabel_FTTx[i]['price']),
                link = cabel_FTTx[i]['link'],
            ).save()
    lock.release()
    print(f'cabel {fttx}')


#парсинг
def parse_ADSS(volokn, lock):
    cabel_ADSS = []
    proc = os.getpid()
    html = get_html('https://shop.nag.ru/catalog/01919.opticheskij-kabel/06006.podvesnoj-samonesuschij-adss')
    kN = get_kN(html.text)
    print(volokn, kN, proc)
    for kn in kN:
        html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/06006.podvesnoj-samonesuschij-adss?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc')
        if html.status_code == 200:
            page_count = get_page(html.text)
            for page in range(1, page_count+1):
                print(f'Идет парсинг страницы {page} из {page_count}')
                html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/06006.podvesnoj-samonesuschij-adss?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc', params= {'page': page})
                cabel_ADSS.extend(get_content(html.text, volokn, kn))
        else:
            print('Error', proc)
    #print(cabel_ADSS[0])
    #return cabel_ADSS
    lock.acquire()
    for i in range(0, len(cabel_ADSS)):
       try:
           adss = ADSS.objects.get(link = cabel_ADSS[i]['link'])
           adss.name = cabel_ADSS[i]['name']
           adss.volokno = int(cabel_ADSS[i]['volokna'])
           adss.kN = cabel_ADSS[i]['kN']
           adss.price = int(cabel_ADSS[i]['price'])
           adss.save()
       except ADSS.DoesNotExist:
           adss = ADSS(
                name = cabel_ADSS[i]['name'],
                volokno = int(cabel_ADSS[i]['volokna']),
                kN = cabel_ADSS[i]['kN'],
                price = int(cabel_ADSS[i]['price']),
                link = cabel_ADSS[i]['link'],
            ).save()
    lock.release()
    print(f'cabel {adss}')


def parse_tip8(volokn, lock):
    cabel_tip8 = []
    proc = os.getpid()
    html = get_html('https://shop.nag.ru/catalog/01919.opticheskij-kabel/02701.podvesnoj-tip-8')
    kN = get_kN(html.text)
    print(volokn, kN, proc)
    for kn in kN:
        html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/02701.podvesnoj-tip-8?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc')
        if html.status_code == 200:
            page_count = get_page(html.text)
            for page in range(1, page_count+1):
                print(f'Идет парсинг страницы {page} из {page_count}')
                html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/02701.podvesnoj-tip-8?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc', params= {'page': page})
                cabel_tip8.extend(get_content(html.text, volokn, kn))
        else:
            print('Error', proc)
    #return cabel_tip8
    lock.acquire()
    for i in range(0, len(cabel_tip8)):
        try:
            tip8 = Tip8.objects.get(link=cabel_tip8[i]['link'])
            tip8.name = cabel_tip8[i]['name']
            tip8.volokno = int(cabel_tip8[i]['volokna'])
            tip8.kN = cabel_tip8[i]['kN']
            tip8.price = int(cabel_tip8[i]['price'])
            tip8.save()
        except Tip8.DoesNotExist:
            tip8 = Tip8(
                name=cabel_tip8[i]['name'],
                volokno=int(cabel_tip8[i]['volokna']),
                kN=cabel_tip8[i]['kN'],
                price=int(cabel_tip8[i]['price']),
                link=cabel_tip8[i]['link'],
            ).save()
    lock.release()


def parse_kanalizaciy(volokn, lock):
    cabel_kanaliz = []
    proc = os.getpid()
    #print(proc)
    html = get_html('https://shop.nag.ru/catalog/01919.opticheskij-kabel/02287.v-kanalizatsiyu')
    #volokn = get_volokno(html.text)
    kN = get_kN(html.text)
    print(volokn, kN, proc)
    for kn in kN:
        html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/02287.v-kanalizatsiyu?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc')
        if html.status_code == 200:
            page_count = get_page(html.text)
            for page in range(1, page_count+1):
                print(f'Идет парсинг страницы {page} из {page_count}')
                html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/02287.v-kanalizatsiyu?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc', params= {'page': page})
                cabel_kanaliz.extend(get_content(html.text, volokn, kn))
        else:
            print('Error', proc)
    #print(cabel_kanaliz)
    lock.acquire()
    for i in range(0, len(cabel_kanaliz)):
        try:
            vkanal = Vkanal.objects.get(link=cabel_kanaliz[i]['link'])
            vkanal.name = cabel_kanaliz[i]['name']
            vkanal.volokno = int(cabel_kanaliz[i]['volokna'])
            vkanal.kN = cabel_kanaliz[i]['kN']
            vkanal.price = int(cabel_kanaliz[i]['price'])
            vkanal.save()
        except Vkanal.DoesNotExist:
            vkanal = Vkanal(
                name=cabel_kanaliz[i]['name'],
                volokno=int(cabel_kanaliz[i]['volokna']),
                kN=cabel_kanaliz[i]['kN'],
                price=int(cabel_kanaliz[i]['price']),
                link=cabel_kanaliz[i]['link'],
            ).save()
    lock.release()


def parse_grunt(volokn, lock):
    cabel_grunt = []
    proc = os.getpid()
    #print(proc)
    html = get_html('https://shop.nag.ru/catalog/01919.opticheskij-kabel/28001.v-grunt')
    #volokn = get_volokno(html.text)
    kN = get_kN(html.text)
    print(volokn, kN, proc)
    for kn in kN:
        html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/28001.v-grunt?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc')
        if html.status_code == 200:
            page_count = get_page(html.text)
            for page in range(1, page_count+1):
                print(f'Идет парсинг страницы {page} из {page_count}')
                html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/28001.v-grunt?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc', params= {'page': page})
                cabel_grunt.extend(get_content(html.text, volokn, kn))
        else:
            print('Error', proc)
    #print(cabel_grunt)
    lock.acquire()
    for i in range(0, len(cabel_grunt)):
        try:
            vgrunt = Vgrunt.objects.get(link=cabel_grunt[i]['link'])
            vgrunt.name = cabel_grunt[i]['name']
            vgrunt.volokno = int(cabel_grunt[i]['volokna'])
            vgrunt.kN = cabel_grunt[i]['kN']
            vgrunt.price = int(cabel_grunt[i]['price'])
            vgrunt.save()
        except Vgrunt.DoesNotExist:
            vgrunt = Vgrunt(
                name=cabel_grunt[i]['name'],
                volokno=int(cabel_grunt[i]['volokna']),
                kN=cabel_grunt[i]['kN'],
                price=int(cabel_grunt[i]['price']),
                link=cabel_grunt[i]['link'],
            ).save()
    lock.release()


def parse_raspredelitelnyj(lock):
    cabel_raspredelitelnyj = []
    html = get_html('https://shop.nag.ru/catalog/01919.opticheskij-kabel/02388.raspredelitelnyj')
    volokn = get_volokno(html.text)
    print(volokn)
    for volokno in volokn:
        html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/02388.raspredelitelnyj?count=20&default_view=2&filter_147_{volokno}=true&in_stock=&page=1&sort=popularity_desc')
        if html.status_code == 200:
            page_count = get_page(html.text)
            for page in range(1, page_count+1):
                print(f'Идет парсинг страницы {page} из {page_count}')
                html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/02388.raspredelitelnyj?count=20&default_view=2&filter_147_{volokno}=true&in_stock=&page=1&sort=popularity_desc', params= {'page': page})
                cabel_raspredelitelnyj.extend(get_content(html.text, volokno))
        else:
            print('Error')
    #print(cabel_raspredelitelnyj)
    lock.acquire()
    for i in range(0, len(cabel_raspredelitelnyj)):
        try:
            raspred = Raspredelitelnyj.objects.get(link=cabel_raspredelitelnyj[i]['link'])
            raspred.name = cabel_raspredelitelnyj[i]['name']
            raspred.volokno = int(cabel_raspredelitelnyj[i]['volokna'])
            raspred.kN = cabel_raspredelitelnyj[i]['kN']
            raspred.price = int(cabel_raspredelitelnyj[i]['price'])
            raspred.save()
        except Raspredelitelnyj.DoesNotExist:
            raspred = Raspredelitelnyj(
                name=cabel_raspredelitelnyj[i]['name'],
                volokno=int(cabel_raspredelitelnyj[i]['volokna']),
                kN=cabel_raspredelitelnyj[i]['kN'],
                price=int(cabel_raspredelitelnyj[i]['price']),
                link=cabel_raspredelitelnyj[i]['link'],
            ).save()
    lock.release()


def parse_ognestojkij(volokn, lock):
    cabel_ognestojkij = []
    proc = os.getpid()
    #print(proc)
    html = get_html('https://shop.nag.ru/catalog/01919.opticheskij-kabel/28170.ognestojkij')
    #volokn = get_volokno(html.text)
    kN = get_kN(html.text)
    print(volokn, kN, proc)
    for kn in kN:
        html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/28170.ognestojkij?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc')
        if html.status_code == 200:
            page_count = get_page(html.text)
            for page in range(1, page_count+1):
                print(f'Идет парсинг страницы {page} из {page_count}')
                html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/28170.ognestojkij?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc', params= {'page': page})
                cabel_ognestojkij.extend(get_content(html.text, volokn, kn))
        else:
            print('Error', proc)
    #print(cabel_ognestojkij)
    lock.acquire()
    for i in range(0, len(cabel_ognestojkij)):
        try:
            ogne = Ognestojkij.objects.get(link=cabel_ognestojkij[i]['link'])
            ogne.name = cabel_ognestojkij[i]['name']
            ogne.volokno = int(cabel_ognestojkij[i]['volokna'])
            ogne.kN = cabel_ognestojkij[i]['kN']
            ogne.price = int(cabel_ognestojkij[i]['price'])
            ogne.save()
        except Ognestojkij.DoesNotExist:
            ogne = Ognestojkij(
                name=cabel_ognestojkij[i]['name'],
                volokno=int(cabel_ognestojkij[i]['volokna']),
                kN=cabel_ognestojkij[i]['kN'],
                price=int(cabel_ognestojkij[i]['price']),
                link=cabel_ognestojkij[i]['link'],
            ).save()
    lock.release()


def parse_universalnyj(volokn, lock):
    cabel_universalnyj = []
    proc = os.getpid()
    #print(proc)
    html = get_html('https://shop.nag.ru/catalog/01919.opticheskij-kabel/34484.universalnyj')
    #volokn = get_volokno(html.text)
    kN = get_kN(html.text)
    print(volokn, kN, proc)
    for kn in kN:
        html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/34484.universalnyj?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc')
        if html.status_code == 200:
            page_count = get_page(html.text)
            for page in range(1, page_count+1):
                print(f'Идет парсинг страницы {page} из {page_count}')
                html = get_html(f'https://shop.nag.ru/catalog/01919.opticheskij-kabel/34484.universalnyj?count=20&default_view=2&filter_147_{volokn}=true&filter_148_{kn}=true&in_stock=&page=1&sort=popularity_desc', params= {'page': page})
                cabel_universalnyj.extend(get_content(html.text, volokn, kn))
        else:
            print('Error', proc)
    #print(cabel_universalnyj)
    lock.acquire()
    for i in range(0, len(cabel_universalnyj)):
        try:
            univers = Universalnyj.objects.get(link=cabel_universalnyj[i]['link'])
            univers.name = cabel_universalnyj[i]['name']
            univers.volokno = int(cabel_universalnyj[i]['volokna'])
            univers.kN = cabel_universalnyj[i]['kN']
            univers.price = int(cabel_universalnyj[i]['price'])
            univers.save()
        except Universalnyj.DoesNotExist:
            univers = Universalnyj(
                name=cabel_universalnyj[i]['name'],
                volokno=int(cabel_universalnyj[i]['volokna']),
                kN=cabel_universalnyj[i]['kN'],
                price=int(cabel_universalnyj[i]['price']),
                link=cabel_universalnyj[i]['link'],
            ).save()
    lock.release()


def main():
    lock = Lock()
    list = [parse_FTTx, parse_raspredelitelnyj]
    proces = []
    for item in list:
        p = Process(target=item, args=(lock,))
        proces.append(p)
        p.start()



    html_def = []

    html_list = ['https://shop.nag.ru/catalog/01919.opticheskij-kabel/06006.podvesnoj-samonesuschij-adss', 'https://shop.nag.ru/catalog/01919.opticheskij-kabel/02701.podvesnoj-tip-8',
                'https://shop.nag.ru/catalog/01919.opticheskij-kabel/02287.v-kanalizatsiyu', 'https://shop.nag.ru/catalog/01919.opticheskij-kabel/28001.v-grunt', 'https://shop.nag.ru/catalog/01919.opticheskij-kabel/28170.ognestojkij',
                'https://shop.nag.ru/catalog/01919.opticheskij-kabel/34484.universalnyj']

    def_list = [parse_ADSS, parse_tip8, parse_kanalizaciy, parse_grunt, parse_ognestojkij, parse_universalnyj]

    i = 0
    for html in html_list:

        html_def.append({
            'html' : html,
            'def' : def_list[i]
        })
        i += 1


    # result = []
    # for item in html_def:
    #     time.sleep(1)
    #     print(item['html'] , item['def'])
    #     htmltext = get_html(item['html']).text
    #     volokno = get_volokno(htmltext)
    #     pool = Pool(processes=(len(volokno)+1))
    #     result.append(pool.map_async(item['def'], volokno))
    #     pool.close()
    #     proces.append(pool)


    for item in html_def:
        time.sleep(1)
        htmltext = get_html(item['html']).text
        volokno = get_volokno(htmltext)
        for volokn in volokno:
            p = Process(target=item['def'], args=(volokn, lock))
            proces.append(p)
            p.start()


    for proc in proces:
        proc.join()

    #print(result[0].get())

#класс команды
class Command(BaseCommand):
    help = 'Parser'

    def handle(self, *args, **options):
        t1 = time.time()
        main()
        t2 = time.time()
        print(t2 - t1)


if __name__ == '__main__':
    com = Command()
    com.handle()
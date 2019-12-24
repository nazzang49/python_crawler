import os
import time
from datetime import datetime
import ssl
import sys
from itertools import count
from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_pelicana():
    results=[]
    for page in count(start=1):
        # 페이지 번호 문자열 포맷
        url = 'https://pelicana.co.kr/store/stroe_search.html?page=%d&branch_name=&gu=&si='%page
        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class':'table mt20'})
        tag_tbody = tag_table.find('tbody')
        # tbody 안의 모든 tr 추출
        tags_tr = tag_tbody.findAll('tr')

        # 더 이상 데이터가 없는 경우
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            # 가장 앞 두 문자열만 추출
            sidogu = address.split()[:2]
            results.append((name, address) + tuple(sidogu))

    # 저장
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    # table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)


def crawling_nene():
    results = []
    before = ''
    page=1
    while True:
        # 페이지 번호 문자열 포맷
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d'%page
        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_names = bs.findAll(attrs={'class': 'shopName'})
        tag_adds = bs.findAll(attrs={'class': 'shopAdd'})

        # 현재 페이지의 가장 첫 점포 이름 저장
        now = tag_names[0].text

        # 페이지를 이동했는데, 가장 처음 점포 이름이 같다면 = 종료
        if now == before:
            break
        before = now

        for i in range(0,len(tag_names)):
            sidogu = tag_adds[i].text.split()[:2]
            results.append((tag_names[i].text,tag_adds[i].text)+tuple(sidogu))

        page+=1

    # 저장
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])

    finalResult = []

    cnt = 0
    for name in table['name']:

        if name.count('강원') >= 1:
            cnt+=1

    if cnt > 60:
        finalResult.append('Y')

    testTable = pd.DataFrame(finalResult, columns=['critical issue'])

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULT_DIR = f'{BASE_DIR}/__results__'
    print(BASE_DIR)

    testTable.to_csv('__results__/testForMonitoring.csv', encoding='utf-8', mode='w', index=True)
    table.to_csv('__results__/nene.csv', encoding='utf-8', mode='w', index=True)

def crawling_kyochon():
    results = []
    for sido in range(1,118):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch='%(sido, sido2)
            html = crawler.crawling(url)

            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul',attrs={'class': 'list'})
            tag_spans = bs.findAll(attrs={'class': 'store_item'})

            for tag_span in tag_spans:
                strings = list(tag_span.strings)
                name = strings[1]
                # 공백 및 개행 제거
                addr = strings[3].strip('\r\n\t')
                sidogu = addr.split()[:2]

                results.append((name, addr) + tuple(sidogu))

    for t in results:
        print(t)

    # 저장
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    # table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)

def crawling_goobne():
    results = []
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('/cafe24/chromedriver/chromedriver.exe')
    wd.get(url)
    time.sleep(2)

    for page in count(start=1):
        # 자바스크립트 실행
        script = 'store.getList(%d)'%page
        wd.execute_script(script)
        print(f'{datetime.now()}: success for request [{url}]')
        time.sleep(2)

        # 실행결과 HTML(동적으로 렌더링 된)추출
        html = wd.page_source

        # 파싱
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody',attrs={'id': 'store_list'})
        tag_trs = tag_tbody.findAll('tr')

        if tag_trs[0].get('class') is None:
            break

        for tag_tr in tag_trs:
            strings = list(tag_tr.strings)
            name = strings[1]
            addr = strings[6]
            sidogu = addr.split()[:2]
            results.append((name, addr)+tuple(sidogu))

    wd.quit()
    for i in results:
        print(i)

    # 저장
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    # table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)

import matplotlib.pyplot as plt
import seaborn as sns

def getTestCsv():
    df = pd.read_csv('D:/python_crawler/__results__/testForMonitoring.csv')
    print(df.dropna().head())
    cnt = 0
    if df['critical issue'][0] == 'Y':
        cnt = 1

    plt.hist(cnt)
    plt.show()


if __name__  == '__main__':
    # pelicana
    # crawling_pelicana()

    # nene
    # crawling_nene()

    # get CSV file
    getTestCsv()

    # kyochon
    # crawling_kyochon()

    # goobne
    # crawling_goobne()
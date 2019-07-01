from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from collection import crawler


def ex01():
    # 1. 통신 요청 및 html 태그 추출
    request = Request('http://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    response = urlopen(request)
    html = response.read().decode('cp949')
    # print(html)

    # 2. 파싱 작업
    bs = BeautifulSoup(html, 'html.parser')
    # print(bs.prettify())
    divs = bs.findAll('div', attrs={'class':'tit3'})
    # print(divs)

    # 3. 순회(제목, 순위, 링크 출력)
    for index, div in enumerate(divs):
        print(index+1, div.a.text, div.a['href'], sep=' : ')

def proc_naver_movie_rank(data):
    bs = BeautifulSoup(data, 'html.parser')
    # print(bs.prettify())
    results = bs.findAll('div', attrs={'class': 'tit3'})
    return results

# 출력 함수이더라도, 리턴값 표시
def store_naver_movie_rank(data):
    for index, div in enumerate(data):
        print(index+1, div.a.text, div.a['href'], sep=' : ')
    return data

def ex02():
    result = crawler.crawling(
        url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
        encoding='cp949',
        proc1=proc_naver_movie_rank,
        proc2=lambda data:list(map(lambda div:print(div.a.text, div.a['href']), sep=':'),enumerate(data))
    )

 # ex01()의 반환값 = none(false), not이 붙어있으면 true
__name__ == '__main__' and not \
    ex01() and not \
    ex02()















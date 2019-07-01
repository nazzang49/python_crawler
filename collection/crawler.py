import ssl
import sys
from urllib.request import Request, urlopen
from datetime import datetime

# 크롤링 작업 시 중복 요소 함수 작성
# lambda data:data = data 주입 data return (디폴트)
def crawling(url='',
             encoding='utf-8',
             proc1=lambda data:data,
             proc2=lambda data:data,
             err=lambda e:print(f'{e} : {datetime.now()}', file=sys.stderr)):
    try:
        request = Request(url)
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(request)
        print(f'{datetime.now()}: success for request [{url}]')
        receive = response.read()

        # proc1 = html -> 필요한 태그 부분 추출 작업
        # proc2 = 출력 및 저장
        return proc2(proc1(receive.decode(encoding, errors='replace')))
    except Exception as e:
        err(e)

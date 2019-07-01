# beautifulsoup 사용
from bs4 import BeautifulSoup

html = '''<td class="title black">
<div class="tit3" id="my-div">
<a href="/movie/bi/mi/basic.nhn?code=161967" title="기생충">기생충</a>
</div>
</td>'''

# 1. 태그 조회
def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    # print(bs)
    # print(type(bs))
    tag = bs.a
    print(tag)
    print(type(tag))

    tag = bs.td.div
    print(tag)
    print(type(tag))

# 2. 속성값 가져오기(attribute)
def ex2():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.td
    # 공백이 존재하면 따로 구분하여 원소 처리 = 리스트
    print(tag['class'])

    tag = bs.div
    # 존재하지 않는 키값을 입력하면 에러 발생
    # print(tag['id'])
    print(tag.attrs)

# 3. 속성값으로 태그 조회
def ex3():
    bs = BeautifulSoup(html, 'html.parser')

    # class 값에 title이 포함되는 태그 찾기
    tag = bs.find('td',attrs={'class':'title'})
    print(tag)

    tag = bs.find(attrs={'class': 'tit3'})
    print(tag)

if __name__ == '__main__':
    # ex1()
    # ex2()
    ex3()













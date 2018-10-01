import urllib3
from bs4 import BeautifulSoup #정규식을 안써도되게 해주는 paser.
import sys
import os

from urllib.parse import quote
#'quote'는 'urlopen'에서 인자로 사용되는 URL주소(타겟 주소)에 한글(UTF_8)이 포함되었을 때, 이를 아스키(ASCII)형식으로 바꿔주기 위한 함수
TARGET_URL_BEFORE_KEYWORD = "https://www.sciencedirect.com/search?qs=" #검색어 입력.
TARGET_URL_BEFORE_OFFSET = '&offset=' #25씩 증가시켜야됨.
if not os.path.exists('./title_of_paper'):
    os.makedirs('./title_of_paper')


# https://www.sciencedirect.com/search?qs=stroke&offset=100
# 1번 함수 : 논문  내용 긁어오기. 2번 함수 내부에서  링크 주소 받아 들어가서 사용되는 함수.
###################################1.3
def get_text(URL):
    http = urllib3.PoolManager()
    source_code_from_url = http.request('GET', URL).data

    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    title_of_paper = soup.select('span.title-text')
    abstract_of_paper = soup.select('div.abstract author')
    #    keywords_of_paper = soup.select('div.keyword')
    #    authors_of_paper = soup.select('span.text surname')
    #    contents_of_paper = soup.select('div.Body')
    ###################################1.4
    for title, abs in zip(title_of_paper,abstract_of_paper):
        string_title = str(title.get_text(":"))
        string_abs = str(title.get_text())

        if ':' in string_title:
            title_list = string_title.split(':')
            string_title = ';'.join(title_list)
        with open("./title_of_paper/%s.csv" % (string_title), 'w+') as file:
            file.write(str(string_title)+ '\n')
            file.write(str(string_abs)+ '\n')
            file.close()

# 2번 함수 :각각의 논문의 링크를 가져오는 코드.

def get_link_from_title(offset_num, URL):
    ##############################################1.1
    for i in range(offset_num):  ###################################2,3,4,5,6,7...
        current_offset = (i - 1) * 25
        position = URL.index('&')
        URL_with_offset = URL + str(current_offset)

        http = urllib3.PoolManager()
        source_code_from_URL = http.request('GET', URL_with_offset).data
        soup = BeautifulSoup(source_code_from_URL, 'lxml',
                             from_encoding='utf-8')
        ############################################1.2
        for title in soup.find_all('div', 'result-item-content'):
            title_link = title.select('a')
            article_URL = 'https://www.sciencedirect.com' + title_link[0]['href']
            # 링크가 생략되어있어서 앞에  "https://www.sciencedirect.com" 를 붙여줘야함.
            get_text(article_URL)  ###################################1.3


# 메인함수

def main(argv):
    if len(argv) != 3:
        print("python 프로젝트_ScienceDirect_Spider.py [검색어] [페이지 몇 까지]라고 치세요.")
        return
    keyword = argv[1]
    offset_num = int(argv[2])
    target_URL = TARGET_URL_BEFORE_KEYWORD + quote(keyword) + TARGET_URL_BEFORE_OFFSET

    get_link_from_title(offset_num, target_URL)  # 2번 함수




if __name__ == '__main__':
    main(sys.argv)

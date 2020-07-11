import requests
from bs4 import BeautifulSoup

#HTTP Get Request
req = requests.get('https://college.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000005587/list.do')
#html 소스 가져오기
html = req.text

soup = BeautifulSoup(html, 'html.parser')
#print(soup)


#txt > div > div.no-more-tables > table > tbody > tr > td.subject > a
#txt > div > div.no-more-tables > table > tbody > tr > td.subject > a
#txt > div > div.no-more-tables > table > tbody > tr > td.subject > a
#txt > div > div.no-more-tables > table > tbody > tr:nth-child(1) > td.subject > a

notice_title = soup.select(
    '#txt > div > div.no-more-tables > table > tbody > tr > td.subject > a'
)
notice_date = soup.select(
    '#txt > div > div.no-more-tables > table > tbody > tr > td.Date'
)

data = {}

for title in notice_title:
    print(title)
    #print(title.get('onclick'))
    #data[title.text] = title.get('javascript')

for notice in notice_date:
    print(notice.text)




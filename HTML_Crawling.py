import requests
from bs4 import BeautifulSoup

#HTTP Get Request
req = requests.get('https://www.google.com')
#html 소스 가져오기
html = req.text


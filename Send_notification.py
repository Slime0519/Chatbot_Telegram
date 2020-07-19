import telegram
import requests
import os
from bs4 import BeautifulSoup
import HTML_API_TOKEN

mytokenclass = HTML_API_TOKEN()
MY_TOKEN = mytokenclass.GetToken

url = 'https://api.telegram.org/bot{}/sendMessage'.format(MY_TOKEN)

req = requests.get("https://college.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000005587/list.do")
req.encoding = 'utf-8'




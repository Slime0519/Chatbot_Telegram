from HTML_API_TOKEN import API_TOKEN
import requests
import json

#토큰 받아오기
MyToken = API_TOKEN()
token = MyToken.GetToken()

#봇의 메시지 내용 가져오기 : https://core.telegram.org/bots/api
url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
#url = 'https://api.telegram.org/bot{}/getMe'.format(token)
response = json.loads(requests.get(url).text)

#sendMessage method : 메시지 보내기
url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)

#response parsing해서 id, text따오기
chat_id = response['result'][-1]['message']['from']['id']
chat_text = response['result'][-2]['message']['text']

print(chat_id)

#send message
requests.get(url, params={'chat_id':chat_id, 'text':"i'm junmyeong bot"})



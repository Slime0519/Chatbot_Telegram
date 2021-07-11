import requests
from bs4 import BeautifulSoup
import os
import telegram
import private_infomation

FilePath = '../article_list'

My_TOKEN_class = private_infomation.API_TOKEN()
MY_TOKEN = My_TOKEN_class.GetToken()

bot = telegram.Bot(token=MY_TOKEN)

if __name__ == "__main__":

    chat_id = bot.getUpdates()[-1].message.chat.id


    req = requests.get("https://college.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000005587/list.do")
    req.encoding = 'utf-8'

    html = req.text

    parser = BeautifulSoup(html, 'html.parser')
    post_names = parser.select('#txt > div > div.no-more-tables > table > tbody > tr > td.subject > a')

    namelist_lastest =[]
    for post_name in post_names:
        namelist_lastest.append(post_name.text)
    namelist_lastest = set(namelist_lastest) #중복 원소 제거
    namelist_lastest = list(namelist_lastest)

    print("<lastest>")
    print(namelist_lastest)
    namelist_before = []
    total_notice_string = "<학내공지 목록>"
    with open(os.path.join(FilePath,'article_name_list.txt'),'r+') as f:
        while 1:
            name_before = f.readline()
            if not name_before : break
            namelist_before.append(name_before[:-1])
        print(namelist_before)
        print(namelist_lastest)
        complement = list(set(namelist_lastest) - set(namelist_before))
        print(complement)
        if complement:
            bot.sendMessage(chat_id=chat_id, text='exist new article')

            print("lastest")
            print(set(namelist_lastest))
            print("before")
            print(set(namelist_before))
            print()
            print(complement)
            total_notice_string = total_notice_string[1:]
            total_notice_string = "<업데이트된 " + total_notice_string
            for i, newname in enumerate(complement):
                total_notice_string = total_notice_string + '\n' + str(i + 1) + '. ' + newname
            # bot.sendMessage(chat_id=chat_id, text=total_notice_string)
            # for newname in complement:
            #   bot.sendMessage(chat_id = chat_id, text = newname+'\n')
        else:
            bot.sendMessage(chat_id=chat_id, text='not exist new article')
            for i, prename in enumerate(namelist_before):
                total_notice_string = total_notice_string + '\n' + str(i + 1) + '. ' + prename

        bot.sendMessage(chat_id=chat_id, text=total_notice_string)
        f.close()


    with open(os.path.join(FilePath,'article_name_list.txt'),'w+') as f:
        for name in namelist_lastest:
            f.write(name+'\n')
        f.close()
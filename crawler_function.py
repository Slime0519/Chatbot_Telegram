import requests
from bs4 import BeautifulSoup
import os
import telegram
import HTML_API_TOKEN

FilePath = 'article_list'

def remove_repetition(list):
    templist = []
    for element in list:
        if not element in templist:
            templist.append(element)
    return templist

def get_lastest_notice():
    req = requests.get("https://college.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000005587/list.do")
    req.encoding = 'utf-8'

    html = req.text

    parser = BeautifulSoup(html, 'html.parser')
    post_names = parser.select('#txt > div > div.no-more-tables > table > tbody > tr > td.subject > a')

    namelist_lastest = []
    for post_name in post_names:
        namelist_lastest.append(post_name.text)
    namelist_lastest = remove_repetition(namelist_lastest)  # 중복 원소 제거
    namelist_lastest = list(namelist_lastest)

    return namelist_lastest


def save_new_notice(namelist_lastest):
    with open(os.path.join(FilePath,'article_name_list.txt'),'w+') as f:
        for name in namelist_lastest:
            f.write(name+'\n')
        f.close()


def update_notice(complement):
    notice_header = "<업데이트된 학내공지 목록>"
    total_notice_string = notice_header
    for i, newname in enumerate(complement):
        total_notice_string = total_notice_string + '\n' + str(i + 1) + '. ' + newname
    return total_notice_string

def print_notice(bot, chat_id = 'lastest', newarticlecheck = 0):
    namelist_before = []

    if chat_id == 'lastest':
        chat_id = bot.getUpdates()[-1].message.chat.id

    namelist_lastest = get_lastest_notice()

    with open(os.path.join(FilePath,'article_name_list.txt'),'r+') as f:
        while 1:
            name_before = f.readline()
            if not name_before : break
            namelist_before.append(name_before[:-1])
        complement = list(set(namelist_lastest) - set(namelist_before))
        if complement:
            bot.sendMessage(chat_id=chat_id, text='exist new article')
            total_notice_string = update_notice(complement)
        else:
            bot.sendMessage(chat_id=chat_id, text='not exist new article')
            if newarticlecheck: #check만 할 경우 바로 종료
                return

            total_notice_string = "<학내공지 목록>"
            for i, prename in enumerate(namelist_before):
                total_notice_string = total_notice_string + '\n' + str(i + 1) + '. ' + prename

        bot.sendMessage(chat_id=chat_id, text=total_notice_string)
        save_new_notice(namelist_lastest)
        f.close()


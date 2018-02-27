import requests
import datetime
from lxml import html
from bs4 import BeautifulSoup

class ScheduleBot:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=1):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
            return last_update
        else:
            self.get_updates(timeout=100)
            return False



sch_bot = ScheduleBot('520432008:AAE4yCI7R9CVo1iR22yTe0RXMFvJZynvqPM')
def check_schedule(url,group):
      r = requests.get(url)
      soup = BeautifulSoup(r.content, "html.parser")
      res = []
      r = []
      d = []
      m = ''
      for row in soup.findAll('tr'):
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            res.append([ele for ele in cols if ele])
      res = res[1:]
      for div in soup.findAll('div', {'align':'center'}):
            d.append(div.text)
      day = " ".join(d[:2])
      m += day + '\n'
      for x in res:
            if(group in x):
                  r.append(x)
      if(r):
            for x in r:
                  s = " ".join(x[1:])
                  m = m + s + '\n'
            return m
      else:
            return False



def main():
      new_offset = None
      while True:
            sch_bot.get_updates(new_offset)
            last_update = sch_bot.get_last_update()
            if(last_update != False):
                last_update_id = last_update['update_id']
                group = last_update['message']['text'].upper()
                last_chat_id = last_update['message']['chat']['id']
                links = ['http://ftp.sttec.yar.ru/pub/timetable/rasp_second.html','http://ftp.sttec.yar.ru/pub/timetable/rasp_first.html']
                message = check_schedule(links[0],group)
                if(message == False):
                    message = check_schedule(links[1],group)
                    if(message == False):
                            message = 'Для группы {g} замен в расписании не найдено'.format(g = group)
                sch_bot.send_message(last_chat_id,message)
                new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
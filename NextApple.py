from NewsReader import NewsReader

import bs4
import time
from random import randint


class NextApple(NewsReader):
    def __init__(self) -> None:
        super().__init__()
        self.url = 'https://tw.nextapple.com/realtime/latest/'
        self.source = "nextapple"

    def get_news_by_index(self, index, date=None):
        # 指定加载⻚面
        tmpUrl = self.url + str(index) if index else self.url
        print(tmpUrl)
        self.browser.get(tmpUrl)

        # 停留1至3秒
        time.sleep(randint(1, 3))

        objSoup = bs4.BeautifulSoup(self.browser.page_source, 'lxml')
        items = objSoup.find('div', {'class': 'stories-container'})
        items = items.select('.post-style3')
        counts = len(items)
        list = []
        for i in range(counts):
            if items[i].select('time').__len__() > 0 and items[i].select('.post-title').__len__() > 0:
                times = items[i].select('time')[0].text
                if date != None and times.startswith(date) == False:
                    continue
                title = items[i].select('.post-title')[0].text
                link = items[i].select('.post-title')[0].get('href')

                dict = {}
                dict['times'] = times
                dict['title'] = title
                dict['link'] = link
                content = self.get_news_content_by_url(link)
                dict['source'] = self.source
                dict.update(content)
                self.newsDB.insert(dict)

                list.append(dict)

        return list

    def get_news_content_by_url(self, url):
        print(url)
        self.browser.get(url)

        # 停留1至3秒
        time.sleep(randint(1, 3))

        objSoup = bs4.BeautifulSoup(self.browser.page_source, 'lxml')
        items = objSoup.find('div', {'id': 'main-content'})

        dict = {}
        # dict['title'] = items.header.h1.text
        # dict['summary'] = items.header.blockquote.div.text
        content = items.find('div', {'class': 'post-content'})
        para = content.select('p')
        text = ''
        for p in para:
            if p.text != '':
                if p.text.startswith('爆料網址') or p.text.startswith('★加入《壹蘋》Line') or p.text.startswith('★Facebook'):
                    continue
                if p.text.startswith('爆料信箱') or p.text.startswith('★下載《壹蘋新聞網》APP') or p.text.startswith('☞壹蘋'):
                    continue
                if p.text.startswith('★更多相關新聞') or p.text.startswith('★更多相關報導') or p.text.startswith('★更多相關影音'):
                    continue
                if p.text.startswith('推薦新聞') or p.text.startswith(' 推薦新聞')
                    continue
                text += p.text + '\n'

        dict['content'] = text

        return dict

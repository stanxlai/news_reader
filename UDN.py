from NewsReader import NewsReader

import bs4
import time
from random import randint


class UDN(NewsReader):
    def __init__(self) -> None:
        super().__init__()
        self.url = 'https://udn.com/news/breaknews/'
        self.source = "udn"

    def get_news_by_index(self, index, date=None):
        # 指定加载⻚面
        tmpUrl = self.url + str(index) if index else self.url
        print(tmpUrl)
        self.browser.get(tmpUrl)

        # 停留1至3秒
        time.sleep(randint(1, 3))

        objSoup = bs4.BeautifulSoup(self.browser.page_source, 'lxml')

        items = objSoup.find('div', 'context-box__content')
        # 停留1至3秒
        time.sleep(randint(1, 3))

        items = items.select('.story-list__text')
        counts = len(items)
        list = []
        for i in range(counts):
            times = items[i].select('time.story-list__time')
            news = items[i].select('h2 a')
            if news.__len__() > 0 and times.__len__() > 0:
                if date != None and times[0].text.startswith(date) == False:
                    continue
                dict = {}
                dict['times'] = times[0].text
                dict['title'] = news[0].text
                dict['link'] = news[0].get('href') if news[0].get('href').startswith(
                    'https') else 'https://udn.com' + news[0].get('href')
                content = self.get_news_content_by_url(dict['link'])
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
        items = objSoup.find('section', {'class': 'article-content__wrapper'})
        if items == None:
            return {}
        dict = {}
        # dict['title'] = items.select_one('.article-content__title').text
        text = '';
        para = items.select_one('.article-content__editor').select('p')
        for p in para:
            if p.text != None and p.text != '':
                text += p.text.strip() + '\n'
                continue
        dict['content'] = text

        return dict

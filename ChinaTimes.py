from NewsReader import NewsReader

import bs4
import time
from random import randint


class ChinaTimes(NewsReader):
    def __init__(self) -> None:
        super().__init__()
        self.url = 'https://www.chinatimes.com/realtimenews/?page={index:n}&chdtv'
        self.source = "chinatimes"

    def get_news_by_index(self, index, date=None):
        if index > 10:
            return []
        
        # 指定加载⻚面
        tmpUrl = self.url.format(index=index) if index else self.url
        print(tmpUrl)
        self.browser.get(tmpUrl)

        # 停留1至3秒
        time.sleep(randint(1, 3))

        objSoup = bs4.BeautifulSoup(self.browser.page_source, 'lxml')
        itemObj = objSoup.find('section', 'article-list')
        time.sleep(randint(1, 3))

        itemObj = itemObj.select('div.articlebox-compact')
        list = []
        for item in itemObj:
            news = item.select('h3.title a')
            times = item.select('time')
            if (news.__len__() > 0 and times.__len__() > 0):
                if date != None and times[0].get('datetime').startswith(date) == False:
                    continue

                dict = {}
                dict['times'] = times[0].get('datetime')
                dict['title'] = news[0].text
                dict['link'] = news[0].get('href') if news[0].get('href').startswith(
                    'https') else 'https://www.chinatimes.com' + news[0].get('href')
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
        items = objSoup.find('div', {'class': 'column-wrapper'})

        dict = {}
        # dict['title'] = items.select_one('.article-header').text
        para = items.select_one('.article-body').select('p')
        text = ''
        for p in para:
            if p.text != '':
                text += p.text.strip() + '\n'
                continue
        dict['content'] = text
        return dict

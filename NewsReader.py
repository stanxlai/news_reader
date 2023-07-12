# 导入selenium包
from selenium import webdriver
from selenium.webdriver.common.by import By

from abc import ABCMeta, abstractmethod
from NewsDBSqlite import NewsDBSqlite

class NewsReader(metaclass=ABCMeta):
    def __init__(self) -> None:
        # 建立Chrome瀏覽器物件
        self.options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")  # 最大化視窗
        self.options.add_argument("--headless")  # 如果不想打开浏览器界面，可以运行在headless模式

        # 打开Chrome浏览器
        self.browser = webdriver.Chrome(options=self.options)
        self.newsDB = NewsDBSqlite()

        pass

    def __del__(self):
        if self.newsDB != None:
            self.newsDB.close()
        self.browser.quit()

    def get_news(self, count=10, date=None):

        self.news = []
        for i in range(count):
            retValue = self.get_news_by_index(i + 1, date)
            if retValue == None:
                continue
            self.news.extend(retValue)


        return self.news

    @abstractmethod
    def get_news_by_index(self, index, date=None):
        pass

import sqlite3


class NewsDBSqlite:
    def __init__(self, db = 'news.db'):
        self.conn = sqlite3.connect(db)
        try:
            self.conn.execute("select * from news")
        except:
            sql = '''Create table news(  
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                times TEXT,
                title TEXT,
                link TEXT,
                source TEXT,
                content TEXT)'''
            self.conn.execute(sql) # 執行SQL指令

    def insert(self, item):
        sqlStr = "insert into news (times, title, link, source, content) values (?, ?, ?, ?, ?)"
        self.conn.execute(
            sqlStr, (item['times'], item['title'], item['link'], item['source'], item['content']))
        self.conn.commit()

    def readAll(self):
        sqlStr = "select * from news"
        results = self.conn.execute(sqlStr)
        return results

    def readBySource(self, source):
        sqlStr = "select * from news where source = ?"
        cursor = self.conn.cursor()
        cursor.execute(sqlStr, (source,))
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def close(self):
        self.conn.close()

newsDB = NewsDBSqlite()
rows = newsDB.readAll()
rows = newsDB.readBySource('nextapple')
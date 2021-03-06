# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from journal.items import ArticleItem, CategoryItem, NewsItem, PrincipalItem, FrontItem
import psycopg2
import json
import journal.settings as settings


class JournalPipeline:

    def __init__(self):
        self.connection = psycopg2.connect(
            host=settings.POSTGRES_HOSTNAME, 
            user=settings.POSTGRES_USERNAME, 
            password=settings.POSTGRES_PASSWORD, 
            dbname=settings.POSTGRES_DBNAME,
            port=settings.POSTGRES_PORT)

    
    def open_spider(self, spider):
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", item)

        if type(item) is FrontItem:
            test = json.dumps(dict(item))
            self.cursor.execute("INSERT INTO front_page (page) values (%s);", [test])

        if type(item) is ArticleItem:
                self.cursor.execute(
                    "INSERT INTO article (url, category, created_at, article) values (%s, %s, %s, %s);", 
                    [item['url'], item['category'], item['created_at'], json.dumps(dict(item['news']))])

        if type(item) is CategoryItem:
                for news in item["news"]:
                    self.cursor.execute(
                        "INSERT INTO news (url) values (%s);", [news["url"]])

        self.connection.commit()
        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
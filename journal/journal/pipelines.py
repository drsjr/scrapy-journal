# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
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
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",item)

        test = json.dumps(dict(item))

        self.cursor.execute("INSERT INTO principal (main_page) values (%s);", [test])
        self.connection.commit()
        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
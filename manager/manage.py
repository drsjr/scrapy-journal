import os
import psycopg2
import json

POSTGRES_HOSTNAME = "192.168.15.35"
POSTGRES_PORT = 5432
POSTGRES_USERNAME = "folha"
POSTGRES_PASSWORD = "folha"
POSTGRES_DBNAME = "folha"


connection = psycopg2.connect(
            host=POSTGRES_HOSTNAME, 
            user=POSTGRES_USERNAME, 
            password=POSTGRES_PASSWORD, 
            dbname=POSTGRES_DBNAME,
            port=POSTGRES_PORT)

category_spider_api_call = 'curl http://192.168.15.35:6800/schedule.json -d project=journal -d spider=categories -d category={0}'
category_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=categories -d category={0}'

principal_spider_api_call = 'curl http://192.168.15.35:6800/schedule.json -d project=journal -d spider=principal'
principal_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=principal'

categories = [ 'ultimas', 'jundiai', 'opiniao', 'politica', 'economia', 'policia', 'esportes', 'cultura', 'hype']
front_page_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=frontpage'

article_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=article -d category={0}'


def call_all_categories():
    for c in categories:
        os.system(category_spider_api_call_local.format(c))

def call_principal():
    os.system(principal_spider_api_call_local)

def call_front_page():
    os.system(front_page_spider_api_call_local)


def call_article_from_front_page():
    cursor = connection.cursor()

    cursor.execute("SELECT f.page FROM front_page f ORDER BY _id DESC LIMIT 1", [])

    value = cursor.fetchone()[0]

    news_list_url = []
    news_list_url.append(value['main_news']['url'])
    for news in value['column_news']:
        news_list_url.append(news['url'])

    for news in value['carrossel']:
        news_list_url.append(news['url'])

    for url in news_list_url:
        os.system(article_spider_api_call_local.format(url))
    cursor.close()
    connection.close()


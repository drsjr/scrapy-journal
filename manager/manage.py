from typing import List
import psycopg2
import manage_scrapy as scrapy

POSTGRES_HOSTNAME = "172.17.0.2"
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

all_categories = ["ultimas", "jundiai", "opiniao", "politica", "economia", "policia", "esportes", "cultura", "hype"]


def call_all_categories(categories: List[str]):
    for c in categories:
        scrapy.request_crawling_for_category(c)


def call_front_page():
    scrapy.request_crawling_for_front_page()
    

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
        scrapy.request_crawling_for_article(url)


        #cursor.execute("SELECT n.url FROM news n", [])
        #categories_url = cursor.fetchall()
        #for url in categories_url:
        #    scrapy.request_crawling_for_article(url)


    cursor.close()
    connection.close()


def all_calls():
    #
    # python3 -c 'import manage; manage.all_calls()'
    #
    call_front_page()
    call_all_categories(all_categories)
    call_article_from_front_page()



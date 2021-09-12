import os
from typing import List
import psycopg2
import json
import requests

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


LIST_JOBS = 'http://localhost:6800/listjobs.json?project=journal'

category_spider_api_call = 'curl http://192.168.15.35:6800/schedule.json -d project=journal -d spider=categories -d category={0}'
principal_spider_api_call = 'curl http://192.168.15.35:6800/schedule.json -d project=journal -d spider=principal'

all_categories = ["ultimas", "jundiai", "opiniao", "politica", "economia", "policia", "esportes", "cultura", "hype"]

category_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=categories -d category={0}'
front_page_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=frontpage'
article_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=article -d path={0}'


def list_jobs():
    #
    # curl http://localhost:6800/listjobs.json?project=journal | python3 -m json.tool
    #
    list_jobs_request = requests.get(LIST_JOBS)
    return list_jobs_request.json()


def call_all_categories(categories: List[str]):
    #
    # curl http://localhost:6800/schedule.json -d project=journal -d spider=categories -d category={0} | python3 -m json.tool
    #
    for c in categories:
        payload = [('project', 'journal'), ('spider', 'categories'), ('category', c)]
        category_request = requests.post("http://localhost:6800/schedule.json", data=payload)
        print(category_request.json())


def call_front_page():
    #
    # curl http://localhost:6800/schedule.json -d project=journal -d spider=frontpage | python3 -m json.tool
    #
    payload = [('project', 'journal'), ('spider', 'frontpage')]
    front_page_request = requests.post("http://localhost:6800/schedule.json", data=payload)
    return front_page_request.json()


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
        #
        # curl http://localhost:6800/schedule.json -d project=journal -d spider=article -d path={0} | python3 -m json.tool
        #
        payload = [('project', 'journal'), ('spider', 'article'), ('path', url)]
        article_request = requests.post("http://localhost:6800/schedule.json", data=payload)
        print(article_request.json())


    #cursor.execute("SELECT n.url FROM news n", [])
    #categories_url = cursor.fetchall()
    #for url in categories_url:
    #    #
    #    # curl http://localhost:6800/schedule.json -d project=journal -d spider=article -d path={0} | python3 -m json.tool
    #    #
    #    payload = [('project', 'journal'), ('spider', 'article'), ('path', url)]
    #    article_request = requests.post("http://localhost:6800/schedule.json", data=payload)
    #    print(article_request.json())



    cursor.close()
    connection.close()


def all_calls():
    #
    # python3 -c 'import manage; manage.all_calls()'
    #
    call_front_page()
    call_all_categories(all_categories)
    call_article_from_front_page()



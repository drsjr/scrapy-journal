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

#categories = ["ultimas", "jundiai", "opiniao", "politica", "economia", "policia", "esportes", "cultura", "hype"]

category_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=categories -d category={0}'
front_page_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=frontpage'
article_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=article -d path={0}'


def list_jobs():
    """
        curl http://localhost:6800/listjobs.json?project=journal

    """
    list_jobs_request = requests.get(LIST_JOBS)
    value = list_jobs_request.json()
    print(value)


def call_all_categories(categories: List[str]):
    """
        curl http://localhost:6800/schedule.json -d project=journal -d spider=categories -d category={0}

    """
    for c in categories:
        payload = [('project', 'journal'), ('spider', 'categories'), ('category', c)]
        list_jobs_request = requests.post("http://localhost:6800/schedule.json", data=payload)
        print(list_jobs_request.json())


def call_front_page():
    """
        curl http://localhost:6800/schedule.json -d project=journal -d spider=frontpage

    """
    payload = [('project', 'journal'), ('spider', 'frontpage')]
    list_jobs_request = requests.post("http://localhost:6800/schedule.json", data=payload)
    return list_jobs_request.json()


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


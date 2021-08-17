import os
from typing import Dict
import psycopg2
import json

POSTGRES_HOSTNAME = "192.168.15.35"
POSTGRES_PORT = 5432
POSTGRES_USERNAME = "folha"
POSTGRES_PASSWORD = "folha"
POSTGRES_SCRAPY_DBNAME = "scrapy_jj"
POSTGRES_DATABASE_DBNAME = "database_jj"


connection = psycopg2.connect(
            host=POSTGRES_HOSTNAME, 
            user=POSTGRES_USERNAME, 
            password=POSTGRES_PASSWORD, 
            dbname=POSTGRES_SCRAPY_DBNAME,
            port=POSTGRES_PORT)

connection2 = psycopg2.connect(
            host=POSTGRES_HOSTNAME, 
            user=POSTGRES_USERNAME, 
            password=POSTGRES_PASSWORD, 
            dbname=POSTGRES_DATABASE_DBNAME,
            port=POSTGRES_PORT)

scrapy = connection.cursor()
database = connection2.cursor()




"""
    sh: 
        python3 -c 'import etl_scrapy_database as etl; etl.get_all_url()'
"""
def get_all_url():
    scrapy.execute("SELECT url FROM article;", [])
    all_urls = scrapy.fetchall()
    
    for url in all_urls:
        if url[0] is not None:
            get_article_from_url(url[0])


    scrapy.close()
    connection.close()


"""
    sh: 
        python3 -c 'import etl_scrapy_database as etl; etl.get_article_from_url("/jundiai/2021/08/130082-nova-ubs-jardim-do-lago-tera-atendimento-a-populacao-geral.html")'
"""
def get_article_from_url(url: str):
    if (verify_url(url)):
        scrapy.execute("SELECT * FROM article WHERE url = %s;", [url])
        article = scrapy.fetchone()
        insert_article_database(article[1], article[2], article[4])

    else:
        pass


"""
    sh: 
        python3 -c 'import etl_scrapy_database as etl; etl.verify_url("/jundiai/2021/08/130082-nova-ubs-jardim-do-lago-tera-atendimento-a-populacao-geral.html")'
"""
def verify_url(url: str) -> bool:
    database.execute("SELECT url FROM article WHERE url = %s;", [url])
    value = database.fetchone()
    return (value is None)



def insert_article_database(url: str, category: str, article: Dict):
    count = 1

    database.execute("SELECT id FROM category WHERE name = %s;", [category])
    category_id = database.fetchone()[0]
    print("&&&&&&&&&&&&&&&&&&", category_id)


    INSERT_INTO_ARTICLE = """
        INSERT INTO article (url, title, subtitle, image, created_at, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    database.execute(INSERT_INTO_ARTICLE, 
        [url, article["title"], article["subtitle"], article["url_image"], article["time"], category_id])

    database.execute("SELECT id FROM article WHERE url = %s;", [url])
    article_id = database.fetchone()[0]
    print("$$$$$$$$$$$$$$$$$$$$$", article_id)


    INSERT_INTO_PARAGRAPH = """
        INSERT INTO paragraph (article_id, \"order\", paragraph)
        VALUES (%s, %s, %s)
    """

    for p in article['paragraphs']:
        if p is not None and len(p.strip()) > 0:
            database.execute(INSERT_INTO_PARAGRAPH, [article_id, count, p])
            print("$$$$$$$$$$$$$$$$$$$$$", count, p)
            count = count + 1

        else:
            continue

    connection2.commit()


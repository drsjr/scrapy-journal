import os
from typing import Dict
import psycopg2
from datetime import datetime, date

POSTGRES_HOSTNAME = "172.17.0.2"
POSTGRES_PORT = 5432
POSTGRES_USERNAME = "folha"
POSTGRES_PASSWORD = "folha"
POSTGRES_SCRAPY_DBNAME = "folha"

#POSTGRES_HOSTNAME_T = "172.17.0.2"
#POSTGRES_PORT_T = 5432
#POSTGRES_USERNAME_T = "folha"
#POSTGRES_PASSWORD_T = "folha"
#POSTGRES_DATABASE_DBNAME_T = "journal_jj"


connection = psycopg2.connect(
            host=POSTGRES_HOSTNAME, 
            user=POSTGRES_USERNAME, 
            password=POSTGRES_PASSWORD, 
            dbname=POSTGRES_SCRAPY_DBNAME,
            port=POSTGRES_PORT)

connection2 = psycopg2.connect(
            host=POSTGRES_HOSTNAME_T, 
            user=POSTGRES_USERNAME_T, 
            password=POSTGRES_PASSWORD_T, 
            dbname=POSTGRES_DATABASE_DBNAME_T,
            port=POSTGRES_PORT_T)

scrapy = connection.cursor()
database = connection2.cursor()



# 
#  sh: 
#      python3 -c 'import etl_scrapy_database as etl; etl.all_calls()'
# 
def all_calls():
    get_all_url()
    insert_front_page()
    

#
# sh: 
#     python3 -c 'import etl_scrapy_database as etl; etl.get_all_url()'
#
def get_all_url():
    scrapy.execute("SELECT url FROM article;", [])
    all_urls = scrapy.fetchall()
    
    for url in all_urls:
        if url[0] is not None:
            print(url[0])
            get_article_from_url(url[0])



# 
#  sh: 
#      python3 -c 'import etl_scrapy_database as etl; etl.get_article_from_url("/jundiai/2021/08/130082-nova-ubs-jardim-do-lago-tera-atendimento-a-populacao-geral.html")'
# 
def get_article_from_url(url: str):
    print("verify::", str(verify_url(url)))
    if (verify_url(url)):
        scrapy.execute("SELECT * FROM article WHERE url = %s;", [url])
        article = scrapy.fetchone()
        insert_article_database(article[1], article[2], article[4])
        print("INSERTED::", url)
    else:
        pass


#
# sh: 
#     python3 -c 'import etl_scrapy_database as etl; etl.verify_url("/jundiai/2021/08/130082-nova-ubs-jardim-do-lago-tera-atendimento-a-populacao-geral.html")'
#
def verify_url(url: str) -> bool:
    database.execute("SELECT url FROM article WHERE url = %s;", [url])
    value = database.fetchone()
    print("verify::", url, "\n")
    return (value is None)



def insert_article_database(url: str, category: str, article: Dict):
    count = 1

    database.execute("SELECT id FROM category WHERE name = %s;", [category])
    category_id = database.fetchone()[0]


    INSERT_INTO_ARTICLE = """
        INSERT INTO article (url, title, subtitle, image, created_at, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    database.execute(INSERT_INTO_ARTICLE, 
        [url, article["title"], article["subtitle"], article["url_image"], article["time"], category_id])

    database.execute("SELECT id FROM article WHERE url = %s;", [url])
    article_id = database.fetchone()[0]


    INSERT_INTO_PARAGRAPH = """
        INSERT INTO paragraph (article_id, \"order\", paragraph)
        VALUES (%s, %s, %s)
    """

    for p in article['paragraphs']:
        if p is not None and len(p.strip()) > 0:
            database.execute(INSERT_INTO_PARAGRAPH, [article_id, count, p])
            count = count + 1

        else:
            continue

    connection2.commit()


#
# sh: 
#     python3 -c 'import etl_scrapy_database as etl; etl.insert_front_page()'
#
def insert_front_page():

    scrapy.execute("SELECT created_at, f.page FROM front_page f ORDER BY _id DESC LIMIT 1", [])
    front_page = scrapy.fetchone()

    INSERT_INTO_FRONT_PAGE = """
        INSERT INTO front_page (created_at) VALUES (%s);
    """

    INSERT_INTO_NEWS_MAIN = """
        INSERT INTO news_main (front_page_id, article_id) VALUES (%s, %s);
    """

    INSERT_INTO_NEWS_COLUMN = """
        INSERT INTO news_column (front_page_id, article_id) VALUES (%s, %s);
    """

    INSERT_INTO_NEWS_CARROSSEL = """
        INSERT INTO news_carrossel (front_page_id, article_id) VALUES (%s, %s);
    """

    SELECT_ARTICLE_BY_URL = """
        SELECT id FROM article WHERE url = %s;"""


    database.execute(INSERT_INTO_FRONT_PAGE, [str(front_page[0])]) 
    database.execute("SELECT id from front_page WHERE created_at = %s", [str(front_page[0])])
    front_page_id = database.fetchone()[0]


    main_news = front_page[1]['main_news']
    database.execute(SELECT_ARTICLE_BY_URL, [main_news["url"]])
    article_id = database.fetchone()[0]

    
    if verify_news_main(front_page_id, article_id):
        database.execute(INSERT_INTO_NEWS_MAIN, [front_page_id, article_id])


    #
    # Column News Insert
    #
    for news in front_page[1]['column_news']:
        database.execute(SELECT_ARTICLE_BY_URL, [news["url"]])
        article_id = database.fetchone()[0]
        if verify_news_column(front_page_id, article_id):
            database.execute(INSERT_INTO_NEWS_COLUMN, [front_page_id, article_id])

    #
    # Carrossel News Insert
    #
    for news in front_page[1]['carrossel']:
        database.execute(SELECT_ARTICLE_BY_URL, [news["url"]])
        article_id = database.fetchone()[0]
        if verify_news_column(front_page_id, article_id):
            database.execute(INSERT_INTO_NEWS_CARROSSEL, [front_page_id, article_id])

    connection2.commit()


def verify_news_main(front_page_id: int, article_id: int) -> bool:
    database.execute("SELECT id FROM news_main WHERE front_page_id = %s AND article_id = %s", [front_page_id, article_id])
    value = database.fetchone()
    return (value is None)

def verify_news_column(front_page_id: int, article_id: int) -> bool:
    database.execute("SELECT id FROM news_column WHERE front_page_id = %s AND article_id = %s", [front_page_id, article_id])
    value = database.fetchone()
    return (value is None)

def verify_news_carrossel(front_page_id: int, article_id: int) -> bool:
    database.execute("SELECT id FROM news_carrossel WHERE front_page_id = %s AND article_id = %s", [front_page_id, article_id])
    value = database.fetchone()
    return (value is None)


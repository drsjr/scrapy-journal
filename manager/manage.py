import time
import manage_scrapy as scrapy
from etl.database_prod import ProdDatabase
from etl.database_scrapy import ScrapyDatabase

db_prod = ProdDatabase()
db_scrapy = ScrapyDatabase()


def call_crawling_front_page():
    print("start::call_crawling_front_page")
    scrapy.request_crawling_for_front_page()
    
    waiting()

    front = db_scrapy.get_new_url_from_front_page()

    scrapy.request_crawling_for_article(article_path=front["main"])

    for u in front["column"]:
        scrapy.request_crawling_for_article(article_path=u)

    for u in front["carrossel"]:
        scrapy.request_crawling_for_article(article_path=u)

    for u in front["other"]:
        scrapy.request_crawling_for_article(article_path=u)

    waiting()

    if db_prod.verify_article(front["main"]):
        call_insert_article_and_paragraph(url=front["main"])

    for u in front["column"]:
        if db_prod.verify_article(u):
            call_insert_article_and_paragraph(url=u)

    for u in front["carrossel"]:
        if db_prod.verify_article(u):
            call_insert_article_and_paragraph(url=u)

    for u in front["other"]:
        if db_prod.verify_article(u):
            call_insert_article_and_paragraph(url=u)

    call_etl_front_page()

    db_prod.connection.commit()
    print("end::call_crawling_front_page")


def call_etl_front_page():
    print("start::call_etl_front_page")

    front = db_scrapy.get_new_url_from_front_page()

    print("call_etl_front_page::", front)

    db_prod.insert_front_page(front["created_at"])

    front_page_id = db_prod.get_front_page_id()
    
    print("call_etl_front_page::", front_page_id)

    article = db_prod.get_article_by_url(url=front["main"])

    print("call_etl_front_page::\"", front["main"], "\"")


    db_prod.insert_main_news(front_page_id=front_page_id, article_id=article[0])

    for url in front["column"]:
        a = db_prod.get_article_by_url(url=url)
        db_prod.insert_news_carrossel(front_page_id=front_page_id, article_id=a[0])

    for url in front["carrossel"]:
        a = db_prod.get_article_by_url(url=url)
        db_prod.insert_news_column(front_page_id=front_page_id, article_id=a[0])

    for url in front["other"]:
        a = db_prod.get_article_by_url(url=url)
        db_prod.insert_news_other(front_page_id=front_page_id, article_id=a[0])
        
    print("end::call_etl_front_page")


# (257,
# '/politica/2021/09/134797-projeto-combate-a-incendio-florestais-na-serra-do-japi-e-finalista-para-recursos-de-emenda-parlamentar.html',
# 'Política',
# datetime.datetime(2021, 9, 19, 17, 16),
# {'url': '/politica/2021/09/134797-projeto-combate-a-incendio-florestais-na-serra-do-japi-e-finalista-para-recursos-de-emenda-parlamentar.html',
#  'time': '2021-09-19 17:16:00',
#  'title': 'Projeto Combate a Incêndio Florestais na Serra do Japi é finalista para recursos de emenda parlamentar',
#  'category': 'Política',
#  'subtitle': 'Segundo informado no site da deputada, foram mais de 20 mil voto',
#  'url_image': 'https://www.jj.com.br/_midias/jpg/2021/09/19/600x450/1_fogo_na_serra_4-526155.jpeg',
#  'paragraphs': []})
def call_insert_article_and_paragraph(url: str):
    print("start::call_insert_article_and_paragraph")

    if db_prod.verify_article(url):
        article = db_scrapy.get_article_by_url(url)

        category_id = db_prod.get_category_by_name(article[2])
        
        art = article[4]

        db_prod.insert_article(
            url=art["url"],
            title=art["title"],
            subtitle=art["subtitle"],
            image=art["url_image"],
            created_at=str(article[3]),
            category_id=category_id)

        article = db_prod.get_article_by_url(art["url"])

        order = 1

        for paragraph in art["paragraphs"]:
            db_prod.insert_paragraph(article_id=article[0], order=order, paragraph=paragraph)
            order = order + 1
        print("end::call_insert_article_and_paragraph")


def waiting():
    l = False
    while l is False:
        time.sleep(10)
        #print(scrapy.get_all_schedule_job())
        l = scrapy.verify_all_jobs_finished()


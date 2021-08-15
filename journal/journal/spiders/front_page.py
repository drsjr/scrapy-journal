from typing import Dict
import scrapy
from journal.items import FrontItem


class FrontPageSpider(scrapy.Spider):
    count_pages = 1
    name = 'frontpage'
    start_urls = ['https://www.jj.com.br/']


    def parse(self, response):

        content = response.css('section div.content-wrap')[0]
        row = content.css('div.row')[0]

        main_page = FrontItem()
        main_page["main_news"] = dict()
        main_page["carrossel"] = []
        main_page["column_news"] = []

        main_page["main_news"]["url"] = row.css('div.col_full h2 a').xpath('@href').get()

        # Scrapy News Column Main Page
        
        column_news = row.css('div.col_one_third div.ipost')
        for item in column_news:
            news = {
                "url": item.css('div.entry-title h3 a').xpath('@href').get() 
            }
            main_page["column_news"].append(news)

        # Scrapy News Column Main Page

        carrossel = row.css('div.owl-stage-outer div.oc-item')
        for item in carrossel:
            news = {
                "url": item.css('div.portfolio-image a').xpath('@href').get()
            }
            main_page["carrossel"].append(news)

        yield main_page

        

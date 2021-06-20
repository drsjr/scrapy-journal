from typing import Dict
import scrapy
from journal.items import PrincipalItem


class PrincipalSpider(scrapy.Spider):
    count_pages = 1
    name = 'principal'
    start_urls = ['https://www.jj.com.br/']


    def parse(self, response):

        content = response.css('section div.content-wrap')[0]
        row = content.css('div.row')[0]

        main_page = PrincipalItem()
        main_page["main_news"] = dict()
        main_page["carrossel"] = []
        main_page["column_news"] = []
        #{
        #    "main_news": {
        #        "title": row.css('div.col_full h2 a::text').get(),
        #        "subtitle": row.css('div.col_full p::text').get(),
        #        "link": row.css('div.col_full h2 a').xpath('@href').get(),
        #        "tag": row.css('div.col_full h4::text').get()
        #    },
        #    "carrossel": [],
        #    "column_news": []
        #}

        main_page["main_news"]["title"] = row.css('div.col_full h2 a::text').get()
        main_page["main_news"]["subtitle"] = row.css('div.col_full p::text').get()
        main_page["main_news"]["link"] = row.css('div.col_full h2 a').xpath('@href').get()
        main_page["main_news"]["tag"] = row.css('div.col_full h4::text').get()

        # Scrapy News Column Main Page
        column_news = row.css('div.col_one_third div.ipost')
        for item in column_news:
            news = {
                "title": item.css('div.entry-title h3 a::text').get(),
                "subtitle": item.css('p::text').get(),
                "link": item.css('div.entry-title h3 a').xpath('@href').get() 
            }
            main_page["column_news"].append(news)

        # Scrapy News Column Main Page

        carrossel = row.css('div.owl-stage-outer div.oc-item')
        for item in carrossel:
            news = {
                "link": item.css('div.portfolio-image a').xpath('@href').get(),
                "image_linke": item.css('div.portfolio-image a img').xpath('@src').get(),
                "subtitle": item.css('div.portfolio-desc a::text').get() 
            }
            main_page["carrossel"].append(news)

        yield main_page

        

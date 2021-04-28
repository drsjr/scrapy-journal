import scrapy


class UltimasSpider(scrapy.Spider):
    count_pages = 1
    name = 'principal'
    start_urls = ['https://www.jj.com.br/']


    def parse(self, response):


        
        pass

        

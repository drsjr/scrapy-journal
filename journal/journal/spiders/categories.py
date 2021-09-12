from journal.items import CategoryItem
import journal.date_util as util
import scrapy
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 

class CategoriesSpider(scrapy.Spider):
    name = 'categories'

    def __init__(self, *args, **kwargs):
        super(CategoriesSpider, self).__init__(*args, **kwargs)
        self.category = kwargs.get('category')

    def start_requests(self):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", self.category)
        yield scrapy.Request(f'https://www.jj.com.br/{self.category}')


    def parse(self, response):
        item = CategoryItem()
        item["news"] = []
        divs = response.css('div.clearfix')
        content = divs[0]
        for content in divs:
            if content.css('div.entry-title h2 a').xpath('@href').get() is not None:
                news = {
                    "url": content.css('div.entry-title h2 a').xpath('@href').get()
                }
                item["news"].append(news)

        yield item

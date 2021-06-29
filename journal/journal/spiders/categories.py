from journal.items import CategoryItem
from datetime import datetime
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
        item["category"] = self.category
        item["news"] = []
        divs = response.css('div.clearfix')
        content = divs[0]
        for content in divs:
            news ={
                "url_path": content.css('div.entry-title h2 a').xpath('@href').get(),
                "url_image": content.css('div.entry-image a img').xpath('@src').get(),
                "news_title": content.css('div.entry-title h2 a::text').get(),
                "news_time": format_date(content.css('ul.entry-meta li::text').get()),
                "news_subtitle": content.css('div.entry-content p::text').get()
            }

            if news["url_path"] is None:
                continue

            item["news"].append(news)

        yield  item




def format_date(d: str):
    if d is None or len(d.strip()) == 0:
        return ""

    try:
        parse = datetime.strptime(d.strip(), "%d de %B, %Y às %H:%M")
        return datetime.strftime(parse, "%Y-%m-%d %H:%M:%S")
    except Exception:
        pass


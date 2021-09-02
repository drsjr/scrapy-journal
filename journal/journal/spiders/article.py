import scrapy
from journal.items import ArticleItem
import journal.date_util as util
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 

class ArticleSpider(scrapy.Spider):
    name = 'article'

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.path = kwargs.get('path')

    def start_requests(self):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", self.path)
        yield scrapy.Request(f'https://www.jj.com.br{self.path}')

    def parse(self, response):
        item = ArticleItem()

        item['url'] = self.path
        item['category'] = response.css('div.container h1::text').get(default='').strip()

        item['news'] = {
            'url': self.path,
            'category': response.css('div.container h1::text').get(default='').strip(),
            'title': '',
            'subtitle': '',
            'time': '',
            'url_image': '',
            'paragraphs': []
        }

        if len(response.xpath('//section[@id="content"]')) > 0 and response.xpath('//section[@id="content"]')[0] is not None:
            content = response.xpath('//section[@id="content"]')[0]

            item['news']['title'] = content.css('div.entry-title h2::text').get(default='').strip()
            item['news']['subtitle'] = content.css('div.entry-title h3::text').get(default='').strip()

            if len(content.css('ul.entry-meta li')) > 0:
                _date = util.format_date(content.css('ul.entry-meta li::text')[0].get().strip())
                item['created_at'] = _date
                item['news']['time'] = _date

            if len(content.css('div.entry-image a img')) > 0:
                item['news']['url_image'] = content.css('div.entry-image a img')[0].xpath('@src').get(default='')

            item['news']['paragraphs'] = content.css('p.texto::text').getall()

            yield item

        else:
            pass


        

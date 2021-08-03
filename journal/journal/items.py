# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JournalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PrincipalItem(scrapy.Item):
    main_news = scrapy.Field()
    carrossel = scrapy.Field()
    column_news = scrapy.Field()


class NewsItem(scrapy.Item):
    news = scrapy.Field()
    category = scrapy.Field()

class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    category = scrapy.Field()
    created_at = scrapy.Field()
    news = scrapy.Field()

class FrontItem(scrapy.Item):
    main_news = scrapy.Field()
    carrossel = scrapy.Field()
    column_news = scrapy.Field()




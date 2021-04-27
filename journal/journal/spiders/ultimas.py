import scrapy


class UltimasSpider(scrapy.Spider):
    count_pages = 1
    name = 'ultimas'
    start_urls = ['https://www.jj.com.br/index.php?id=/readMore.php&cd_sesit=36&p={0}'.format(count_pages)]


    def parse(self, response):
        divs = response.css('div.clearfix')

        content = divs[0]

        for content in divs:

            url_path = content.css('div.entry-image a').xpath('@href').get()
            url_image = content.css('div.entry-image a img').xpath('@src').get()
            news_title = content.css('div.entry-title h2 a::text').get()
            news_time = content.css('ul.entry-meta li::text').get().strip()
            news_subtitle = content.css('div.entry-content p::text').get().strip()

            yield {
                'url_path': url_path,
                'url_image': url_image,
                'title': news_title,
                'subtitle': news_subtitle,
                'time': news_time
            }
        if self.count_pages < 3:
            self.count_pages = self.count_pages + 1
            yield scrapy.Request('https://www.jj.com.br/index.php?id=/readMore.php&cd_sesit=36&p={0}'.format(self.count_pages), callback=self.parse)


    def parse_news_content(self, response):
        pass

        

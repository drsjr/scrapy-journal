import scrapy


class UltimasSpider(scrapy.Spider):
    count_pages = 1
    name = 'ultimas'
    start_urls = ['https://www.jj.com.br/index.php?id=/readMore.php&cd_sesit=36&p={0}'.format(count_pages)]


    def parse(self, response):
        divs = response.css('div.clearfix')

        content = divs[0]

        all_urls = []

        for content in divs:

            url_path = content.css('div.entry-title h2 a').xpath('@href').get()
            url_image = content.css('div.entry-image a img').xpath('@src').get()
            news_title = content.css('div.entry-title h2 a::text').get()
            news_time = content.css('ul.entry-meta li::text').get().strip()
            news_subtitle = content.css('div.entry-content p::text').get().strip()

            all_urls.append(url_path)

            #yield {
            #    'url_path': url_path,
            #    'url_image': url_image,
            #    'title': news_title,
            #    'subtitle': news_subtitle,
            #    'time': news_time
            #}
        


        for url in all_urls:
            yield scrapy.Request('https://www.jj.com.br{0}'.format(url), callback=self.parse_news_content)

        
        #if self.count_pages < 3:
        #    self.count_pages = self.count_pages + 1
        #    yield scrapy.Request('https://www.jj.com.br{0}'.format(self.count_pages), callback=self.parse)


    def parse_news_content(self, response):

        article = {
            'url': response.url,
            'tag': '',
            'title': '',
            'subtitle': '',
            'time': '',
            'url_image': '',
            'paragraphs': []
        }

        article['tag'] = response.css('div.container h1::text').get(default='').strip()

        if len(response.xpath('//section[@id="content"]')) > 0 and response.xpath('//section[@id="content"]')[0] is not None:
            content = response.xpath('//section[@id="content"]')[0]

            article['title'] = content.css('div.entry-title h2::text').get(default='')
            article['subtitle'] = content.css('div.entry-title h3::text').get(default='')

            if len(content.css('ul.entry-meta li')) > 0:
                article['time'] = content.css('ul.entry-meta li::text')[0].get().strip()

            if len(content.css('div.entry-image a img')) > 0:
                article['url_image'] = content.css('div.entry-image a img')[0].xpath('@src').get()

            article['paragraphs'] = content.css('p.texto::text').getall()

            yield article

        else:
            pass


        
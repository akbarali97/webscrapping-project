import scrapy


class ZomatoKeralaSpider(scrapy.Spider):
    name = 'zomato-kerala'
    allowed_domains = ['www.zomato.com']
    start_urls = ['http://www.zomato.com/']

    def parse(self, response):
        pass

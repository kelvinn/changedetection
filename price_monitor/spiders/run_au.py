import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

TITLE_SELECTOR = "#product-container > div:nth-child(2) > div > div.col-xs-12.col-md-4.product-buy-wrapper > div.product-title > h1 > span:nth-child(2)"  # noqa
PRICE_SELECTOR = "#js-product-information-price > div > span > span > span"


class RunAUSpider(CrawlSpider):
    name = "runningwarehouse.com.au"
    link_extractor = LinkExtractor()
    custom_settings = {'JOBDIR': f'crawls/{name}'}

    allowed_domains = ['runningwarehouse.com.au']
    base_url = "https://www.runningwarehouse.com.au"
    start_urls = [
        'https://www.runningwarehouse.com.au/New_Balance_FuelCell_SuperComp_Trainer_v3/descpage-N3SCTM1.html',
        'https://www.runningwarehouse.com.au/mens-running-shoes.html',
        'https://www.runningwarehouse.com.au/fpw.html',
        'https://www.runningwarehouse.com.au/'
    ]

    rules = [
        Rule(LinkExtractor(), callback='parse_detail_page', follow=True),
    ]

    def parse_detail_page(self, response):
        try:
            price = float(response.xpath('//*[@id="ordering_form"]/div[1]/div[2]/div/div[1]/div/span/mark//text()').extract_first())
            name = str(response.xpath('//*[@id="main_content"]/div/div[1]/div/div[1]/h1//text()').extract_first())
            
            item = {}
            item['url'] = response.url

            item['price'] = price
            item['name'] = name

            return item
        
        except TypeError:
            return None

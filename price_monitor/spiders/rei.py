import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


TITLE_SELECTOR = "#product-container > div:nth-child(2) > div > div.col-xs-12.col-md-4.product-buy-wrapper > div.product-title > h1 > span:nth-child(2)"  # noqa
PRICE_SELECTOR = "#js-product-information-price > div > span > span > span"


class ReiSpider(CrawlSpider):
    name = "rei.com"

    allowed_domains = ['www.rei.com']

    rules = [
        Rule(LinkExtractor(), callback='parse', follow=True),
    ]

    def get_price(self, product):
        offers = product.get('offers')
        return min([float(offer.get('price')) for offer in offers if
                    offer.get('availability') == "https://schema.org/InStock"], default=0)

    def parse(self, response):
        product = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())

        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = product.get('name')
        item['price'] = self.get_price(product) or 0
        return item

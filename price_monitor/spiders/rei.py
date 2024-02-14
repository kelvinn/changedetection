import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

TITLE_SELECTOR = "#product-container > div:nth-child(2) > div > div.col-xs-12.col-md-4.product-buy-wrapper > div.product-title > h1 > span:nth-child(2)"  # noqa
PRICE_SELECTOR = "#js-product-information-price > div > span > span > span"


class ReiSpider(CrawlSpider):
    name = "rei.com"
    link_extractor = LinkExtractor()
    custom_settings = {'JOBDIR': f'crawls/{name}'}

    allowed_domains = ['rei.com']
    base_url = "https://www.rei.com/"
    start_urls = [
        'https://www.rei.com/product/141845/nemo-tensor-insulated-sleeping-pad',
        'https://www.rei.com/c/backpacking-packs',
        'https://www.rei.com/'
    ]

    rules = [
        Rule(LinkExtractor(allow=('product/')), callback='parse_detail_page', follow=True),
        Rule(LinkExtractor(), callback='parse', follow=True)
    ]

    def get_price(self, product):
        offers = product.get('offers')
        price = 0
        if offers:
            price = min([float(offer.get('price')) for offer in offers if offer.get('availability') == "https://schema.org/InStock"], default=0)  # noqa
        return price

    def parse_detail_page(self, response):
        try:
            product = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())

            item = {}
            item['url'] = response.url
            item['title'] = product.get('name')
            item['price'] = self.get_price(product) or 0
            return item
        except TypeError:
            return None

    def parse(self, response):
        self.log(f"Need to create a rule for {response.url}")

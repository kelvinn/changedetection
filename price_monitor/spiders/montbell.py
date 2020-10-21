from .base_spider import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

TITLE_SELECTOR = "#main > main > div > div.product-details > div.product-details__main-column > form > h1::text"
PRICE_SELECTOR = "#main > main > div > div.product-details > div.product-details__main-column > form > p.product-details__price > em"  # noqa

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class MontbellSpider(CrawlSpider):
    name = "montbell.us"
    allowed_domains = ['www.montbell.us']
    base_url = "https://www.montbell.us/"
    start_urls = [
        'https://www.montbell.us/products/index.php?cat_id=2&gen_cd=1',
        'https://www.montbell.us/'
    ]

    rules = [
        Rule(LinkExtractor(), callback='parse', follow=True),
    ]

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css(TITLE_SELECTOR).extract_first("").strip()
        item['price'] = self.get_price(response)

        return item

    def get_price(self, response):
        return float(response.css(PRICE_SELECTOR).re_first(PRICE_REGEX) or 0)

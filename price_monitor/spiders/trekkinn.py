from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

TITLE_SELECTOR = "#parallax > div > div:nth-child(4) > div.detalles > div.info > h1::text"
PRICE_SALE_SELECTOR = "#total_dinamic"
PRICE_STD_SELECTOR = "#precio_anterior"

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class TrekkinnSpider(CrawlSpider):
    name = "trekkinn.com"

    allowed_domains = ['www.trekkinn.com']

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
        price_sale = float(response.css(PRICE_SALE_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_std = float(response.css(PRICE_STD_SELECTOR).re_first(PRICE_REGEX) or 0)
        prices = [price for price in [price_sale, price_std] if price > 0]
        return min(prices) if len(prices) > 0 else 0

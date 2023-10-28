from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

TITLE_SELECTOR = "#parallax > div > div:nth-child(4) > div.detalles > div.info > h1::text"
PRICE_SALE_SELECTOR = "#total_dinamic"
PRICE_STD_SELECTOR = "#precio_anterior"

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class TrekkinnSpider(CrawlSpider):
    name = "trekkinn.com"
    link_extractor = LinkExtractor()

    allowed_domains = ['www.trekkinn.com']
    base_url = "https://www.trekkinn.com/"
    start_urls = [
        'https://www.trekkinn.com/outdoor-mountain/mens-clothing-accessories/3142/s',
        'https://www.trekkinn.com/outdoor-mountain/mens-clothing/3017/lf',
        'https://www.trekkinn.com/outdoor-mountain/mens-clothing-pants/11450/s',
        'https://www.trekkinn.com/outdoor-mountain/mens-shoes/3012/f'
    ]

    rules = [
        Rule(LinkExtractor(), callback='parse', follow=True),
    ]

    def parse_detail_page(self, response):
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

    def parse(self, response):
        self.log(f"Need to create a rule for {response.url}")

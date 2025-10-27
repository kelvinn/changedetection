from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

BRAND_SELECTOR = "body > div.body-wrap > div > article > div.product-overview.js-product-overview > section.product-buybox.js-product-buybox.qa-product-buybox > div.product-buybox-intro > h1 > span::text"  # noqa
TITLE_SELECTOR = "span[data-id='productTitle']::text"  # noqa
PRICE_STD_SELECTOR = """//*[@id="content"]/div/div[3]/section[2]/div[2]/span"""  # noqa
PRICE_SALE_SELECTOR = """//*[@id="content"]/div/div[3]/section[2]/div[2]/span[2]/text()"""  # noqa
PRICE_INACTIVE_SELECTOR = """//*[@id="content"]/div/div[3]/section[2]/div[2]/span[3]"""
PRICE_META_SELECTOR = """//*[@property="product:price:amount"]/@content"""  # noqa

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class BackcountrySpider(CrawlSpider):
    name = "backcountry.com"
    link_extractor = LinkExtractor()
    custom_settings = {'JOBDIR': f'crawls/{name}'}

    allowed_domains = ['backcountry.com']
    base_url = "https://www.backcountry.com/"
    start_urls = [
        'https://www.backcountry.com/cat/mens-footwear?fl=false',
        'https://www.backcountry.com/hike-camp?activity=true&fl=true'
    ]

    rules = [
        Rule(LinkExtractor(), callback='parse', follow=True),
    ]

    rules = [
        Rule(LinkExtractor(allow=('skid')), callback='parse_detail_page', follow=True),
        Rule(LinkExtractor(), callback='parse', follow=True)
    ]

    def parse_detail_page(self, response):
        item = {}
        item['url'] = response.url
        title = response.css(TITLE_SELECTOR).extract_first("").strip()
        item['title'] = title
        item['price'] = self.get_price(response)
        return item

    def get_price(self, response):
        price_sale = float(response.xpath(PRICE_SALE_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_inactive = float(response.xpath(PRICE_INACTIVE_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_std = float(response.xpath(PRICE_STD_SELECTOR).re_first(PRICE_REGEX) or 0)
        prices = [price for price in [price_sale, price_inactive, price_std] if price > 0]
        price = min(prices) if len(prices) > 0 else 0
        if price <= 0:
            m = response.xpath(PRICE_META_SELECTOR).re_first(PRICE_REGEX)
            price = float(m) if m else 0
        return price

    def parse(self, response):
        self.log(f"Need to create a rule for {response.url}")

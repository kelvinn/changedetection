from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

TITLE_SELECTOR = "#product-title::text"
PRICE_STD_SELECTOR = "#hero-pdp__buy > div > div.buy-config__title.sk-init.sk-viewport-in.sk-show-first.sk-show-complete > div > span.js-buy-config-price.buy-config-price > div > span > span > span"
PRICE_SALE_SELECTOR = "#hero-pdp__buy > div > div.buy-config-attributes > div > div:nth-child(1) > div > div > div > a:nth-child(1) > div > div.product-tile__meta > div > div > div > div > span > span > span"
PRICE_MIN_SELECTOR = "#pdpMain > div > div.product-detail > div.price-holder.mobile > div > div > span.min-price"
PRICE_MAX_SELECTOR = "#pdpMain > div > div.product-detail > div.price-holder.mobile > div > div > span.max-price"
PRICE_NOT_SALE_SELECTOR = "#product-content > div.product-price.desktop > span"

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class PatagoniaSpider(CrawlSpider):
    name = "patagonia.com"
    allowed_domains = ['www.patagonia.com']

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
        price_min = float(response.css(PRICE_MIN_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_max = float(response.css(PRICE_MAX_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_std = float(response.css(PRICE_STD_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_not_sale = float(response.css(PRICE_NOT_SALE_SELECTOR).re_first(PRICE_REGEX) or 0)
        prices = [price for price in [price_sale, price_min, price_max, price_std, price_not_sale] if price > 0]
        return min(prices) if len(prices) > 0 else 0

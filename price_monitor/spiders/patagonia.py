from .base_spider import BaseSpider

TITLE_SELECTOR = "#pdpMain > div > div.product-detail > h1::text"
PRICE_STD_SELECTOR = "#pdpMain > div > div.product-detail > div.price-holder.mobile > div > span.price-standard"
PRICE_SALE_SELECTOR = "#pdpMain > div > div.product-detail > div.price-holder.mobile > div > span.price-sales"
PRICE_MIN_SELECTOR = "#pdpMain > div > div.product-detail > div.price-holder.mobile > div > div > span.min-price"
PRICE_MAX_SELECTOR = "#pdpMain > div > div.product-detail > div.price-holder.mobile > div > div > span.max-price"
PRICE_NOT_SALE_SELECTOR = "#product-content > div.product-price.desktop > span"

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class PatagoniaSpider(BaseSpider):
    name = "patagonia.com"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css(TITLE_SELECTOR).extract_first("").strip()
        item['price'] = self.get_price(response)
        yield item

    def get_price(self, response):
        price_sale = float(response.css(PRICE_SALE_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_min = float(response.css(PRICE_MIN_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_max = float(response.css(PRICE_MAX_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_std = float(response.css(PRICE_STD_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_not_sale = float(response.css(PRICE_NOT_SALE_SELECTOR).re_first(PRICE_REGEX) or 0)
        prices = [price for price in [price_sale, price_min, price_max, price_std, price_not_sale] if price > 0]
        return min(prices) if len(prices) > 0 else 0

from .base_spider import BaseSpider

TITLE_SELECTOR = "#parallax > div > div:nth-child(4) > div.detalles > div.info > h1::text"
PRICE_SALE_SELECTOR = "#total_dinamic"
PRICE_STD_SELECTOR = "#precio_anterior"

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class TrekkinnSpider(BaseSpider):
    name = "trekkinn.com"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css(TITLE_SELECTOR).extract_first("").strip()
        item['price'] = self.get_price(response)
        yield item

    def get_price(self, response):
        price_sale = float(response.css(PRICE_SALE_SELECTOR).re_first(PRICE_REGEX) or 0)
        price_std = float(response.css(PRICE_STD_SELECTOR).re_first(PRICE_REGEX) or 0)
        prices = [price for price in [price_sale, price_std] if price > 0]
        return min(prices) if len(prices) > 0 else 0

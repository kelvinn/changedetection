from .base_spider import BaseSpider

TITLE_SELECTOR = "span#productTitle::text"
PRICE_SELECTOR = "span#priceblock_ourprice::text"

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class AmazonSpider(BaseSpider):
    name = "amazon.com"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css(TITLE_SELECTOR).extract_first("").strip()
        item['price'] = float(
            response.css(PRICE_SELECTOR).re_first(PRICE_REGEX) or 0
        )
        yield item
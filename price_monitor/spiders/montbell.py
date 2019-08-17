from .base_spider import BaseSpider

TITLE_SELECTOR = "#main > main > div > div.product-details > div.product-details__main-column > form > h1::text"
PRICE_SELECTOR = "#main > main > div > div.product-details > div.product-details__main-column > form > p.product-details__price > em"


class MontbellSpider(BaseSpider):
    name = "montbell.us"

    # main > main > div > div.product-details > div.product-details__main-column > form > p.product-details__price > em

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css(TITLE_SELECTOR).extract_first("").strip()
        item['price'] = float(response.css(PRICE_SELECTOR).re_first("[-+]?\d*\.\d+|\d+") or 0)
        yield item

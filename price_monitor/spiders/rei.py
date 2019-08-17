from .base_spider import BaseSpider


TITLE_SELECTOR = "#product-container > div:nth-child(2) > div > div.col-xs-12.col-md-4.product-buy-wrapper > div.product-title > h1 > span:nth-child(2)"
PRICE_SELECTOR = "#js-product-information-price > div > span > span > span"


class ReiSpider(BaseSpider):
    name = "rei.com"

    # main > main > div > div.product-details > div.product-details__main-column > form > p.product-details__price > em

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css(TITLE_SELECTOR).extract_first("").strip()
        item['price'] = float(response.css(PRICE_SELECTOR).re_first("[-+]?\d*\.\d+|\d+") or 0)
        yield item
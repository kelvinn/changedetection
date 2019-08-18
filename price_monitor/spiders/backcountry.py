from .base_spider import BaseSpider

BRAND_SELECTOR = "body > div.body-wrap > div > article > div.product-overview.js-product-overview > section.product-buybox.js-product-buybox.qa-product-buybox > div.product-buybox-intro > h1 > span::text"
TITLE_SELECTOR = "body > div.body-wrap > div > article > div.product-overview.js-product-overview > section.product-buybox.js-product-buybox.qa-product-buybox > div.product-buybox-intro > h1::text"
PRICE_STD_SELECTOR = "body > div.body-wrap > div > article > div.product-overview.js-product-overview > section.product-buybox.js-product-buybox.qa-product-buybox > div.product-pricing.js-item-price > span"
PRICE_SALE_SELECTOR = "body > div.body-wrap > div.page.ui-offcanvas-main > article > div.product-overview.js-product-overview > section.product-buybox.js-product-buybox.qa-product-buybox > div.product-pricing.js-item-price > span.product-pricing__sale"
PRICE_INACTIVE_SELECTOR = "body > div.body-wrap > div.page.ui-offcanvas-main > article > div.product-overview.js-product-overview > section.product-buybox.js-product-buybox.qa-product-buybox > div.product-pricing.js-item-price > span.product-pricing__inactive"


class BackcountrySpider(BaseSpider):
    name = "backcountry.com"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        brand = response.css(BRAND_SELECTOR).extract_first("").strip()
        item['title'] = f"""{brand} {response.css(TITLE_SELECTOR).extract_first("").strip()}"""
        item['price'] = self.get_price(response)
        yield item

    def get_price(self, response):
        price_sale = float(response.css(PRICE_SALE_SELECTOR).re_first("[-+]?\d*\.\d+|\d+") or 0)
        price_inactive = float(response.css(PRICE_INACTIVE_SELECTOR).re_first("[-+]?\d*\.\d+|\d+") or 0)
        price_std = float(response.css(PRICE_STD_SELECTOR).re_first("[-+]?\d*\.\d+|\d+") or 0)
        prices = [price for price in [price_sale, price_inactive, price_std] if float(price) > 0]
        return min(prices) if len(prices) > 0 else 0

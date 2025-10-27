from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

TITLE_SELECTOR = "#main > div.product-detail > section:nth-child(1) > div > div.detail-meta-group.grid-span-2.order-3-lg.flex.flex-wrap > h1 > span::text"
PRICE_SELECTOR = "#main > div.product-detail > section:nth-child(1) > div > div.cart-in-container.grid-span-2.order-3-lg.mt-1rem-sm.mt-2\\.5rem-lg > div.delivery-price.mt-1\\.75rem-sm.mt-2\\.5rem-lg > ul > li:nth-child(1) > div > div.price-info.text-right "  # noqa

PRICE_REGEX = "(?<=USD)\\d+(?:\\.\d+)?"  # noqa


class MontbellSpider(CrawlSpider):
    name = "montbell.us"
    link_extractor = LinkExtractor()
    custom_settings = {'JOBDIR': f'crawls/{name}'}

    allowed_domains = ['montbell.com']
    base_url = "https://www.montbell.us/"
    start_urls = [
        'https://www.montbell.com/us/en/products/list?c=4',
        'https://www.montbell.com/us/en/products/list?c=14',
        'https://www.montbell.com/'
    ]

    rules = [
        Rule(LinkExtractor(allow=('products/detail/')), callback='parse_detail_page', follow=True),
        Rule(LinkExtractor(allow=(['list/'])), callback='parse', follow=True)
    ]

    def extract_title(self, response):
        # Primary: the existing specific selector
        title = response.css(TITLE_SELECTOR).extract_first("")
        if title:
            t = str(title).strip()
            if '|' in t:
                t = t.split('|', 1)[0].strip()
            return t

        # Fallback 1: generic h1 text
        texts = response.css('h1::text').getall()
        if texts:
            cleaned = " ".join([t.strip() for t in texts if t and t.strip()])
            if cleaned:
                if '|' in cleaned:
                    cleaned = cleaned.split('|', 1)[0].strip()
                return cleaned

        # Fallback 2: h1 > span::text content
        span_texts = response.css('h1 span::text').getall()
        if span_texts:
            cleaned = " ".join([t.strip() for t in span_texts if t and t.strip()])
            if cleaned:
                if '|' in cleaned:
                    cleaned = cleaned.split('|', 1)[0].strip()
                return cleaned

        # Fallback 3: page title tag
        page_title = response.xpath('//title/text()').get()
        if page_title:
            cleaned = page_title.strip()
            if cleaned:
                if '|' in cleaned:
                    cleaned = cleaned.split('|', 1)[0].strip()
                return cleaned

        return ""

    def parse_detail_page(self, response):
        item = {}
        item['url'] = str(response.url)
        item['title'] = self.extract_title(response)
        item['price'] = self.get_price(response)

        return item

    def get_price(self, response):
        import re
        text = response.text
        # Try to extract USD price from embedded JSON (e.g., "pp_price":"USD285.00")
        price_match = re.search(r'"pp_price"\s*:\s*"USD([0-9]+(?:\.[0-9]+)?)"', text)
        if price_match:
            amount = price_match.group(1)
            try:
                return float(amount)
            except ValueError:
                pass
        # Fallback: look for USD price patterns elsewhere in the HTML
        matches = re.findall(r'(?<=USD)\d+(?:\.\d+)?', text)
        if matches:
            try:
                return float(matches[0])
            except ValueError:
                pass
        # Last resort: attempt to extract via CSS selector
        price = response.css(PRICE_SELECTOR).get()
        if price:
            try:
                return float(price)
            except (ValueError, TypeError):
                pass
        return ""

    def parse(self, response):
        self.log(f"Need to create a rule for {response.url}")

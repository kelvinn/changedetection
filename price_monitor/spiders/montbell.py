from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

TITLE_SELECTOR = "#main > main > div > div.product-details > div.product-details__main-column > form > h1::text"
PRICE_SELECTOR = "#main > main > div > div.product-details > div.product-details__main-column > form > p.product-details__price > em"  # noqa

PRICE_REGEX = "[-+]?\d*\.\d+|\d+"  # noqa


class MontbellSpider(CrawlSpider):
    name = "montbell.us"
    link_extractor = LinkExtractor()
    custom_settings = {'JOBDIR': f'crawls/{name}'}

    allowed_domains = ['montbell.us']
    base_url = "https://www.montbell.us/"
    start_urls = [
        'https://www.montbell.us/products/index.php?cat_id=2&gen_cd=1',
        'https://www.montbell.us/products/list.php?cat_id=25145&gen_cd=1',
        'https://www.montbell.us/'
    ]

    rules = [
        Rule(LinkExtractor(allow=('products/disp.php')), callback='parse_detail_page', follow=True),
        Rule(LinkExtractor(allow=(['list.php', 'index.php'])), callback='parse', follow=True)
    ]

    def parse_detail_page(self, response):
        item = {}
        item['url'] = str(response.url)
        item['title'] = str(response.css(TITLE_SELECTOR).extract_first("").strip())
        item['price'] = self.get_price(response)

        return item

    def get_price(self, response):
        return float(response.css(PRICE_SELECTOR).re_first(PRICE_REGEX) or 0)

    def parse(self, response):
        self.log(f"Need to create a rule for {response.url}")

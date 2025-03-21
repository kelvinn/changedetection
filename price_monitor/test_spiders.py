import unittest
from datetime import datetime
from scrapy.http import Request, TextResponse
from price_monitor.spiders import patagonia, montbell, rei, backcountry, trekkinn, run_au
from models import Price, Product
from price_monitor.pipelines import get_postgres_engine
from sqlalchemy.orm import Session


param_list = [('a', 'a'), ('a', 'b'), ('b', 'b')]
scraper_detail_page_test_criteria = [
    (r'data/montbell_detail.html', 329.0, montbell.MontbellSpider()),
    (r'data/montbell_detail_2.html', 44.0, montbell.MontbellSpider()),
    (r'data/patagonia_detail.html', 99.0, patagonia.PatagoniaSpider()),
    (r'data/backcountry_detail.html', 299.99, backcountry.BackcountrySpider()),
    (r'data/rei_detail.html', 98.83, rei.ReiSpider()),
    (r'data/rei_detail_std.html', 149.0, rei.ReiSpider()),
    (r'data/rei_detail_inreach.html', 0, rei.ReiSpider()),
    (r'data/trekkinn_detail.html', 165.99, trekkinn.TrekkinnSpider()),
    (r'data/running_warehouse_au.html', 329.96, run_au.RunAUSpider())
]


class ScraperSubtest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_detail_page(self):
        for filename, expected_price, spider in scraper_detail_page_test_criteria:
            with self.subTest(filename):
                with open(filename) as f:
                    sample = f.read()

                url = 'http://www.example.com'
                response = TextResponse(url=url, request=Request(url=url), body=sample,
                                        encoding='utf-8')

                parsed = spider.parse_detail_page(response)
                self.assertEqual(expected_price, parsed['price'])


# This is for just searching if text has changed.
class DatabaseSubtest(unittest.TestCase):

    def setUp(self):
        engine = get_postgres_engine()
        with Session(engine) as session:
            self.session = session
        self.name = 'Test Product Name'
        self.amount = 12.3

    def tearDown(self):
        self.session.query(Price).filter(Price.amount == str(self.amount)).delete(synchronize_session=False)
        self.session.commit()

        self.session.query(Product).filter(Product.name == self.name).delete(synchronize_session=False)
        self.session.commit()

    def test_database_models(self):

        name = self.name
        amount = self.amount

        product = Product(name=name, url='https://www.rei.com/', created=datetime.now(), last_updated=datetime.now())
        self.session.add(product)

        price = Price(amount=amount, product=product, created=datetime.now())
        self.session.add(price)

        self.session.commit()

        result = self.session.query(Product).filter_by(name=name)

        self.assertEqual(1, result.count())

        first_product = result.first()

        self.assertEqual(amount, first_product.prices[0].amount)


if __name__ == '__main__':
    unittest.main()

import unittest
from scrapy.spiders import Spider
from price_monitor.pipelines import PostgresPipeline
from scrapy.item import Item, Field
import models
from database import SessionLocal


class BasicItem(Item):
    url = Field()
    title = Field()
    price = Field()


class PipelineSubtest(unittest.TestCase):

    pipeline_class = PostgresPipeline
    settings = None

    def cleanup(self):
        product = self.db.query(models.Product).filter_by(name=self.item['title']).one_or_none()
        if product:  # Feels dirty. Tidy up somehow.
            self.db.query(models.Price).filter(models.Price.product_gid == product.gid).delete(synchronize_session=False)
            self.db.query(models.Product).filter(models.Product.name == self.item['title']).delete(synchronize_session=False)
            self.db.commit()

    def setUp(self):
        self.item = BasicItem()
        self.item['url'] = 'https://www.patagonia.com.au/products/mens-micro-puff-jacket-84066-blk'
        self.item['title'] = 'Puffy Jacket'
        self.item['price'] = 99.00

        self.item2 = BasicItem()
        self.item2['url'] = 'https://www.patagonia.com.au/products/mens-micro-puff-jacket-84066-blk'
        self.item2['title'] = 'Puffy Jacket'
        self.item2['price'] = 199.00

        self.db = SessionLocal()
        self.cleanup()

    def tearDown(self):
        self.cleanup()

    def test_duplicate_prices(self):
        spider = Spider(name='spider')
        pipeline = PostgresPipeline()

        ret1 = pipeline.process_item(self.item, spider)
        assert ret1 is not None

        ret2 = pipeline.process_item(self.item, spider)  # Yes, do it twice
        assert ret2 is not None
        
        product = self.db.query(models.Product).filter_by(name=self.item['title']).one_or_none()

        assert len(product.prices) is 1

    def test_non_duplicate_prices(self):
        spider = Spider(name='spider')
        pipeline = PostgresPipeline()

        ret1 = pipeline.process_item(self.item, spider)
        assert ret1 is not None

        ret2 = pipeline.process_item(self.item2, spider)  # Yes, do it twice
        assert ret2 is not None

        ret3 = pipeline.process_item(self.item, spider)  # Yes, do it twice
        assert ret3 is not None

        product = self.db.query(models.Product).filter_by(name=self.item['title']).one_or_none()

        assert len(product.prices) == 3

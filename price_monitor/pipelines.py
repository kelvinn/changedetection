# -*- coding: utf-8 -*-
import pymongo
from price_monitor import settings
from price_monitor.utils import reversed_timestamp, get_product_names
from scrapy.exceptions import DropItem


class CollectionStoragePipeline(object):

    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings.MONGODB_CONNECTION_URL)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
        return item

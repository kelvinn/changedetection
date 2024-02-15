# -*- coding: utf-8 -*-
from datetime import datetime
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Price, Product
from sqlalchemy import desc
from sqlalchemy import select


def get_postgres_engine():
    DATABASE_URL = getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/changedetection')
    engine = create_engine(DATABASE_URL)
    return engine


class CollectionStoragePipeline(object):

    def process_item(self, item, spider):
        return item


class PostgresPipeline:

    def __init__(self):
        pass

    def process_item(self, item, spider):

        engine = get_postgres_engine()

        with Session(engine) as session, session.begin():

            product = session.query(Product).filter_by(url=item.get('url')).one_or_none()

            # Create the product if it does not already exist
            if not product:
                product = Product(name=item.get('title'),
                                  url=item.get('url'),
                                  created=datetime.now(),
                                  last_updated=datetime.now()
                                  )

                session.add(product)

            if len(product.prices) == 0 or len(product.prices) > 0 and product.prices[0].amount != item.get('price'):

                price = Price(amount=item.get('price'), product=product, created=datetime.now())

                session.add(price)
                session.commit()

        return item

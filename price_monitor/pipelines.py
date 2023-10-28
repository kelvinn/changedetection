# -*- coding: utf-8 -*-
from datetime import datetime
from os import getenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Price, Product


def get_postgres_session():
    DATABASE_URL = getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/changedetection')
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class CollectionStoragePipeline(object):

    def process_item(self, item, spider):
        return item


class PostgresPipeline:

    def __init__(self):
        ## Connection Details
        self.session = get_postgres_session()
    
    def process_item(self, item, spider):

        product = self.session.query(Product).filter_by(url=item.get('url')).one_or_none()

        # Create the product if it does not already exist
        if not product:
            product = Product(name=item.get('title'), 
                            url=item.get('url'), 
                            created=datetime.now(), 
                            last_updated=datetime.now()
                            )

            self.session.add(product)

        price = Price(amount=item.get('price'), product=product, created=datetime.now())

        self.session.add(price)

        self.session.commit()

        return item

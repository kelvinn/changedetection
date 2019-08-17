# -*- coding: utf-8 -*-
import os
import json

BOT_NAME = 'price_monitor'
SPIDER_MODULES = ['price_monitor.spiders']
NEWSPIDER_MODULE = 'price_monitor.spiders'

ROBOTSTXT_OBEY = True

SHUB_KEY = os.getenv('$SHUB_KEY')
# if you want to run it locally, replace '999999' by your Scrapy Cloud project ID below
SHUB_PROJ_ID = os.getenv('SHUB_JOBKEY', '999999').split('/')[0]

SHUB_PROJECT_SETTINGS = json.loads(os.getenv('SHUB_SETTINGS', '{}')).get('project_settings')

#if SHUB_SETTINGS:
#    SHUB_PROJECT_SETTINGS = SHUB_SETTINGS.get('project_settings')


MONGODB_DB = SHUB_PROJECT_SETTINGS.get('MONGODB_DB') if SHUB_PROJECT_SETTINGS else 'scrapy'
MONGODB_COLLECTION = SHUB_PROJECT_SETTINGS.get('MONGODB_COLLECTION') if SHUB_PROJECT_SETTINGS else "price_monitor"
MONGODB_CONNECTION_URL = SHUB_PROJECT_SETTINGS.get('MONGODB_CONNECTION_URL') if SHUB_PROJECT_SETTINGS else 'mongodb://scrapy:password@localhost'

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'price_monitor.pipelines.CollectionStoragePipeline': 400,
    'price_monitor.pipelines.MongoDBPipeline': 400,
}

AUTOTHROTTLE_ENABLED = True
# HTTPCACHE_ENABLED = True

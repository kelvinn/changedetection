# -*- coding: utf-8 -*-
import os
import json

BOT_NAME = 'price_monitor'
SPIDER_MODULES = ['price_monitor.spiders']
NEWSPIDER_MODULE = 'price_monitor.spiders'


SHUB_KEY = os.getenv('$SHUB_KEY')
# if you want to run it locally, replace '999999' by your Scrapy Cloud project ID below
SHUB_PROJ_ID = os.getenv('SHUB_JOBKEY', '999999').split('/')[0]

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'price_monitor.pipelines.CollectionStoragePipeline': 400,
    'price_monitor.pipelines.MongoDBPipeline': 400,
}

ROBOTSTXT_OBEY = True

ROTATING_PROXY_BACKOFF_BASE = 60

ROTATING_PROXY_BACKOFF_CAP = 320

DOWNLOAD_DELAY = 5

COOKIES_ENABLED = True

BOT_NAME = 'Price Monitor Side Project'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
}

USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/62.0.3202.89 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
]

PROXY_USER_PASS = os.getenv('PROXY_USER_PASS', None)

if PROXY_USER_PASS:
    ROTATING_PROXY_LIST = [
        f'https://{PROXY_USER_PASS}@us2884.nordvpn.com',
        f'https://{PROXY_USER_PASS}:i53JVGdwLn@au219.nordvpn.com',

    ]
    DOWNLOADER_MIDDLEWARES.update(
        {'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
         'rotating_proxies.middlewares.BanDetectionMiddleware': 620}
    )



AUTOTHROTTLE_ENABLED = True
HTTPCACHE_ENABLED = True

### Set Environment Variables

if 'SHUB_SETTINGS' in os.environ:
    # We're on ScrapingHub
    SHUB_PROJECT_SETTINGS = json.loads(os.getenv('SHUB_SETTINGS', '{}')).get('project_settings')
    MONGODB_DB = SHUB_PROJECT_SETTINGS.get('MONGODB_DB') if SHUB_PROJECT_SETTINGS else 'scrapy'
    MONGODB_COLLECTION = SHUB_PROJECT_SETTINGS.get('MONGODB_COLLECTION') if SHUB_PROJECT_SETTINGS else "price_monitor"
    MONGODB_CONNECTION_URL = SHUB_PROJECT_SETTINGS.get('MONGODB_CONNECTION_URL') if SHUB_PROJECT_SETTINGS else 'mongodb://scrapy:password@localhost'

else:
    # We're somewhere else
    MONGODB_DB = os.getenv('MONGODB_DB', 'scrapy')
    MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', "price_monitor")
    MONGODB_CONNECTION_URL = os.getenv('MONGODB_CONNECTION_URL', 'mongodb://scrapy:password@localhost')

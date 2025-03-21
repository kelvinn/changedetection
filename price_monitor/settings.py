# -*- coding: utf-8 -*-
import os
import json


BOT_NAME = 'price_monitor'
SPIDER_MODULES = ['price_monitor.spiders']
NEWSPIDER_MODULE = 'price_monitor.spiders'


SHUB_KEY = os.getenv('$SHUB_KEY')
# if you want to run it locally, replace '999999' by your Scrapy Cloud project ID below
SHUB_PROJ_ID = os.getenv('SHUB_JOBKEY', '999999').split('/')[0]

if 'SHUB_SETTINGS' in os.environ:
    SHUB_PROJECT_SETTINGS = json.loads(os.getenv('SHUB_SETTINGS', '{}')).get('project_settings')
    os.environ.update(SHUB_PROJECT_SETTINGS)

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'price_monitor.pipelines.CollectionStoragePipeline': 400,
    'price_monitor.pipelines.PostgresPipeline': 400,
}

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 2

COOKIES_ENABLED = True

BOT_NAME = 'Outdoor Price Monitor Side Project - kelvin@kelvinism.com'

LOG_LEVEL = "INFO"

COOKIES_ENABLED = False

RETRY_ENABLED = False

REDIRECT_ENABLED = True  # Keep this as True, or 'scrapy check' will fail

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 100,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 900,
}

USER_AGENTS = [
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'),  # noqa
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

CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2
AUTOTHROTTLE_ENABLED = True
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_ALWAYS_STORE = True
HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS = ["no-store", "no-cache", "must-revalidate"]

CLOSESPIDER_TIMEOUT = 21600
CLOSESPIDER_TIMEOUT_NO_ITEM = 600

DEFAULT_REQUEST_HEADERS = {
    'Accept-Language': 'en-US,en;q=0.9',
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": "Not A(Brand;v=99, Google Chrome;v=121, Chromium;v=121",
    "Sec-Ch-Ua-Platform": "Windows",
    "Connection": "keep-alive",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
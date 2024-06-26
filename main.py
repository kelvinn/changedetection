import yaml
import sys
import os
import requests
import logging
from datetime import datetime, timedelta
import hashlib
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from price_monitor.spiders import montbell, rei, patagonia
from diskcache import Cache
import sentry_sdk
from sentry_sdk.crons import monitor

SENTRY_DSN = os.getenv('SENTRY_DSN')


sentry_sdk.init(
    dsn=SENTRY_DSN,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


CACHE_DIR = os.getenv('CACHE_DIR', '/tmp/data')

cache = Cache(directory=CACHE_DIR)


def back_off(key, delay):
    past = datetime.now() - timedelta(days=delay)

    last_update = cache.get(key)
    return False if not last_update or datetime.fromisoformat(last_update) < past else True


@monitor(monitor_slug='daily-scrape')
def scrape():
    last_run = cache.get("scrapy_last_ran")
    now = datetime.now()
    if not last_run or now-timedelta(days=1) > last_run or not os.getenv('FLY_ALLOC_ID', None):  # If not on fly then always run
        cache.set("scrapy_last_ran", now)

        spiders = [montbell.MontbellSpider, rei.ReiSpider, patagonia.PatagoniaSpider]
        process = CrawlerProcess(get_project_settings())

        for spider in spiders:
            process.crawl(spider)

        process.start()  # blocking call


if __name__ == "__main__":
    scrape()

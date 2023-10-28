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

CACHE_DIR = os.getenv('CACHE_DIR', '/tmp/data')

cache = Cache(directory=CACHE_DIR)


def back_off(key, delay):
    past = datetime.now() - timedelta(days=delay)

    last_update = cache.get(key)
    return False if not last_update or datetime.fromisoformat(last_update) < past else True


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

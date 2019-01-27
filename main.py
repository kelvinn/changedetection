import yaml
import sys
import os
import requests
import redis
from datetime import datetime, timedelta
import http.client
import urllib
import hashlib

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
cache = redis.from_url(REDIS_URL)


class Config:
    def __init__(self):

        with open("websites.yml", 'r') as stream:
            try:
                loaded = yaml.load(stream)
                self.websites = loaded['websites']
                self.pushover = loaded['pushover']
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(0)


def search(url, text):
    session = requests.Session()
    session.headers.update({'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                                          '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})

    response = session.get(url)

    s = response.text

    return True if response.status_code == 200 and s.count('Quick') > 0 else False


def send(website):

        app_token = os.environ.get(c.pushover['app_token'], None)
        user_key = os.environ.get(c.pushover['user_key'], None)

        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.parse.urlencode({
                         "token": app_token,
                         "user": user_key,
                         "message": website['title'],
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        return conn.getresponse()


def back_off(key, delay):
    past = datetime.now() - timedelta(days=delay)

    last_update = cache.get(key)
    if not last_update or datetime.fromisoformat(last_update.decode()) < past:
        cache.set(key, datetime.now().isoformat())
        return False
    else:
        return True


def run():
    for website in c.websites:
        url, text, delay, action = website['url'], website['text'], website['delay'], website['action']
        key = hashlib.sha224(f'{url + text}'.encode()).hexdigest()

        found = search(url, text)
        if (action == 'remove' and not found) or (action == 'added' and found) and not back_off(key, delay):
            send(website)


if __name__ == "__main__":
    c = Config()
    run()

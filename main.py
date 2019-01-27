import yaml
import sys
import os
import requests
import redis
from datetime import datetime, timedelta
import http.client, urllib

cache = redis.Redis(host='localhost', port=6379)


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

    if response.status_code == 200 and s.count(text) > 0:
        return True
    else:
        return False


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


def run():
    for website in c.websites:
        url, text, delay = website['url'], website['text'], website['delay']
        if search(url, text):
            past = datetime.now() - timedelta(days=delay)

            last_update = cache.get(url)
            if not last_update or datetime.fromisoformat(last_update.decode()) < past:
                cache.set(url, datetime.now().isoformat())
                send(website)


if __name__ == "__main__":
    c = Config()
    run()

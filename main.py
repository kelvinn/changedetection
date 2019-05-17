import yaml
import sys
import os
import requests
import redis
import logging
from datetime import datetime, timedelta
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


config = Config()


def search(url, text):
    session = requests.Session()
    session.headers.update({'Accept': 'text/html',
                            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'})

    response = session.get(url)

    s = response.text

    return response.status_code, True if response.status_code == 200 and s.count(text) > 0 else False


def send(key, msg, url):

    app_token = os.environ.get(config.pushover['app_token'], None)
    user_key = os.environ.get(config.pushover['user_key'], None)

    logging.info(f'Sending the msg: {msg}.')
    cache.set(key, datetime.now().isoformat())  # Set a datetime when we sent the message
    r = requests.post('https://api.pushover.net/1/messages.json',
                      data={
                          'token': app_token,
                          'user': user_key,
                          'message': f'<a href="{url}">{msg}</a>',
                          'title': msg
                      })

    return r.status_code


def back_off(key, delay):
    past = datetime.now() - timedelta(days=delay)

    last_update = cache.get(key)
    return False if not last_update or datetime.fromisoformat(last_update.decode()) < past else True


def run(event=None, context=None):
    results = []
    for website in config.websites:
        url, text, delay, action = website['url'], str(website['text']), website['delay'], website['action']
        key = hashlib.sha224(f'{url + str(text)}'.encode()).hexdigest()

        resp_code, found = search(url, text)

        if ((action == 'remove' and not found) or (action == 'added' and found)) and not back_off(key, delay):
            logging.info(f'Change found: {url, text, action} ')
            results.append(send(key=key, msg=website['title'], url=website['url']))

        elif resp_code == 404 and not back_off(key, delay):
            logging.warning(f'404: {url}')
            results.append(send(key, config, f'Page Not Found {text}'))
        else:
            logging.info(f'No change found: {url, text, action}')
    return results


if __name__ == "__main__":
    run()

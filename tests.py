import unittest

import responses
from datetime import datetime
from main import search, back_off, cache, send, Config, run, config


def cleanup():
    cache.delete('1742b2350006e55ba3241d3e0b2926c45150c30ea782d778bc1fce6e')


class AppTestCase(unittest.TestCase):

    def setUp(self):
        cleanup()

    def tearDown(self):
        cleanup()

    @responses.activate
    def test_search(self):
        with open(r'data/patagonia.html') as f:
            sample = f.read()

        responses.add(responses.GET, 'https://www.patagonia.com/shop/web-specials-mens?start=0&sz=72#tile-54',
                      body=sample, status=200)
        result = search(
            'https://www.patagonia.com/shop/web-specials-mens?start=0&sz=72#tile-54', 'Airdini Cap'
        )
        self.assertTrue(result)

    def test_back_off(self):
        key = 'foo'
        cache.set(key, datetime.now().isoformat())

        result = back_off(key, 5)
        self.assertTrue(result)

    @responses.activate
    def test_send(self):

        responses.add(responses.POST, 'https://api.pushover.net/1/messages.json',
                      status=201,
                      json={
                          'status': '1',
                          'request': '647d2300-702c-4b38-8b2f-d56326ae460b'
                      })

        c = Config()
        result = send('1742b2350006e55ba3241d3e0b2926c45150c30ea782d778bc1fce6e', c, 'Test Msg')

        self.assertEqual(201, result)

    @responses.activate
    def test_run(self):
        config.websites = [{'title': 'test',
                            'url': 'https://www.patagonia.com/shop/web-specials-mens',
                            'text': 'Airdini Cap',
                            'action': 'added',
                            'delay': 5}]

        with open(r'data/patagonia.html') as f:
            sample = f.read()

        responses.add(responses.GET, 'https://www.patagonia.com/shop/web-specials-mens',
                      body=sample, status=200)

        responses.add(responses.POST, 'https://api.pushover.net/1/messages.json',
                      status=201,
                      json={
                          'status': '1',
                          'request': '647d2300-702c-4b38-8b2f-d56326ae460b'
                      })

        results = run()
        self.assertEqual(201, results[0])


if __name__ == '__main__':

    unittest.main()


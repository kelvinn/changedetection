import unittest

import responses
from datetime import datetime
from scrapy.http import Request, TextResponse
from main import search, back_off, cache, send, Config, run, config
from price_monitor.spiders import patagonia, montbell, rei, backcountry, trekkinn


def cleanup():
    cache.delete('1742b2350006e55ba3241d3e0b2926c45150c30ea782d778bc1fce6e')


param_list = [('a', 'a'), ('a', 'b'), ('b', 'b')]
scraper_test_criteria = [
    (r'data/montbell_detail.html', 329.0, montbell.MontbellSpider()),
    (r'data/patagonia_detail.html', 89.0, patagonia.PatagoniaSpider()),
    (r'data/backcountry_detail.html', 299.99, backcountry.BackcountrySpider()),
    (r'data/rei_detail.html', 98.83, rei.ReiSpider()),
    (r'data/rei_detail_std.html', 149.0, rei.ReiSpider()),
    (r'data/trekkinn_detail.html', 165.99, trekkinn.TrekkinnSpider())
]


class ScraperSubtest(unittest.TestCase):

    def test_parse(self):
        for filename, expected_price, spider in scraper_test_criteria:
            with self.subTest(filename):
                with open(filename) as f:
                    sample = f.read()

                url = 'http://www.example.com'
                response = TextResponse(url=url, request=Request(url=url), body=sample,
                                        encoding='utf-8')

                parsed = spider.parse(response)
                self.assertEqual(expected_price, next(parsed)['price'])

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
        self.assertTrue(result[1])

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

        result = send('1742b2350006e55ba3241d3e0b2926c45150c30ea782d778bc1fce6e', 'Test Msg', 'https://example.com')

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


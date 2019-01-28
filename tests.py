import unittest

import responses
from datetime import datetime
from main import search, back_off, cache, send, Config


def cleanup():
    pass


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
                      body=sample, status=200,
                      content_type='application/xml')
        result = search(
            'https://www.patagonia.com/shop/web-specials-mens?start=0&sz=72#tile-54', 'Airdini Cap'
        )
        self.assertTrue(result)

    def test_back_off(self):
        key = 'foo'
        cache.set(key, datetime.now().isoformat())

        result = back_off(key, 5)
        self.assertTrue(result)


if __name__ == '__main__':

    unittest.main()


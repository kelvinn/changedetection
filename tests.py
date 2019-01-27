import unittest

import responses
from main import search


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


if __name__ == '__main__':

    unittest.main()


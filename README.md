# Background

![Python package](https://github.com/kelvinn/changedetection/workflows/Python%20package/badge.svg)

Some random things I'm using to track prices of things I may want to buy.

# Local dev prep

* Install Redis (brew install redis)
* pip install -r requirements.txt
* python3 tests.py

# Details for myself later

* Get the CSS / xpath selectors by highlighting the item in Chrome and "Inspect"
* Auto-deploys via Travis
* Can run on Scraping Hub with:
    * shub deploy
    * shub schedule [spider]
* If there are odd errors on Scraping Hub
    * Upgrade the stack in `scrapinghub.yml`
    * Make sure docker is running
    * Pull the relevant image from https://hub.docker.com/r/scrapinghub/scrapinghub-stack-scrapy/tags
    
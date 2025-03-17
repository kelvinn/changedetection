# Background

[![Test and Deploy](https://github.com/kelvinn/changedetection/actions/workflows/main.yml/badge.svg)](https://github.com/kelvinn/changedetection/actions/workflows/main.yml)

Some random things I'm using to track prices of things I may want to buy.

# Local dev prep

* pip install -r requirements.txt
* colima start
* docker compose up
* bash scripts/test.sh
* scrapy check

# Deployment

* Handled by Github Actions


# Notes & Workarounds

* Get the CSS / xpath selectors by highlighting the item in Chrome and "Inspect"
* Update test_spiders.py accordingly along with the respective spiders
* 
    
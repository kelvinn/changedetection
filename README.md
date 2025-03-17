# Background

[![Test and Deploy](https://github.com/kelvinn/changedetection/actions/workflows/main.yml/badge.svg)](https://github.com/kelvinn/changedetection/actions/workflows/main.yml)

Some random things I'm using to track prices of things I may want to buy.

# Local dev prep

* brew install postgresql
* brew services start postgresql@14
* createuser -s postgres
* createdb changedetection
* pip install -r requirements.txt
* bash scripts/test.py

# Deployment

* Handled by Github Actions

# Notes & Workarounds

* Get the CSS / xpath selectors by highlighting the item in Chrome and "Inspect"
* Update test_spiders.py accordingly along with the respective spiders
* 
    
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Stock(scrapy.Item):
    n = scrapy.Field()
    ticker = scrapy.Field()
    company = scrapy.Field()
    sector = scrapy.Field()
    industry = scrapy.Field()
    country = scrapy.Field()
    market_cap = scrapy.Field()
    p_e = scrapy.Field()
    price = scrapy.Field()
    change = scrapy.Field()
    volume = scrapy.Field()

class Option(scrapy.Item):
    ticker = scrapy.Field()
    symbol = scrapy.Field()
    option = scrapy.Field()
    close = scrapy.Field()
    change = scrapy.Field()
    volume = scrapy.Field()
    volume_change = scrapy.Field()
    open_interest = scrapy.Field()
    open_interest_change = scrapy.Field()
    url = scrapy.Field()

class YahooSummary(scrapy.Item):
    ticker = scrapy.Field()
    prev_close = scrapy.Field()
    open = scrapy.Field()
    bid = scrapy.Field()
    ask = scrapy.Field()
    _1y_target_est = scrapy.Field()
    beta = scrapy.Field()
    next_earnings_date = scrapy.Field()
    day_s_range = scrapy.Field()
    _52wk_range = scrapy.Field()
    volume = scrapy.Field()
    avg_vol = scrapy.Field()
    market_cap = scrapy.Field()
    p_e = scrapy.Field()
    eps = scrapy.Field()
    div_yield = scrapy.Field()
    earnings_date = scrapy.Field()
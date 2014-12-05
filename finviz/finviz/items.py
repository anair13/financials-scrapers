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
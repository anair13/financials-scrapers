# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from finviz.items import Option

path = '//*[@id="mediaquotesoptions"]/div[2]/div/div/div/div/table//tr'
PREFIX = "http://finance.yahoo.com"

class FinvizspiderSpider(scrapy.Spider):
    name = "YahooSpider"
    allowed_domains = ["yahoo.com"]
    start_urls = ["http://finance.yahoo.com/options/lists/?mod_id=mediaquotesoptions&tab=tab" 
        + str(i) + "&rcnt=100&page=" + str(j) for i in range(1,7) for j in range(1,3)]

    def parse(self, response):
        data = response.xpath(path)
        for row in data[1:]:
            info = row.xpath('.//td//text()').extract()
            o = Option()
            o['ticker'] = info[0]
            o['symbol'] = info[1]
            o['option'] = info[2]
            o['close'] = info[3]
            o['change'] = info[4]
            o['volume'] = info[5]
            o['volume_change'] = info[6]
            o['open_interest'] = info[7]
            o['open_interest_change'] = info[8]
            o['url'] = PREFIX + row.xpath('//td[@class="stk"]/a/@href').extract()[0]
            yield o
        
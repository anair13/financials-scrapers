# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from finviz.items import Stock

path = '//tr[@class="table-dark-row-cp"]|//tr[@class="table-light-row-cp"]'

class FinvizspiderSpider(scrapy.Spider):
    name = "FinvizSpider"
    allowed_domains = ["finviz.com"]
    start_urls = ["http://finviz.com/screener.ashx?v=111&r=" + str(i) for i in range(1,7002,20)]

    def parse(self, response):
        data = response.xpath(path)
        for row in data:
            info = row.xpath('.//td//text()').extract()
            s = Stock()
            s['n'] = info[0]
            s['ticker'] = info[1]
            s['company'] = info[2]
            s['sector'] = info[3]
            s['industry'] = info[4]
            s['country'] = info[5]
            s['market_cap'] = info[6]
            s['p_e'] = info[7]
            s['price'] = info[8]
            s['change'] = info[9]
            s['volume'] = info[10]
            yield s
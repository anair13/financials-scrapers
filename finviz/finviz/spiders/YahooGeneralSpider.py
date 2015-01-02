# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.shell import inspect_response
from finviz.items import YahooSummary
import MySQLdb
from finviz.slugify import *
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

PREFIX = "http://finance.yahoo.com"

class YahooGeneralSpider(scrapy.Spider):
    name = "YahooGeneralSpider"
    allowed_domains = ["yahoo.com"]

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        # get list of tickers
        DATABASE = ('192.168.1.117', 'scrn01', 'scrn01', 'scrn01')
        conn = MySQLdb.connect(*DATABASE)
        cur = conn.cursor()
        cur.execute('SELECT `stocks`.`TICKER` FROM `scrn01`.`stocks`;')
        names = [i[0] for i in cur.fetchall() if len(i) > 0]

        self.start_urls = [PREFIX + "/q?s=" + ticker for ticker in names]
        self.fields = set()
        self.errors = []

    def parse(self, response):
        """Parse the summary page"""
        # inspect_response(response)
        data = response.xpath('//*[@id="yfi_quote_summary_data"]/table/tr')
        y = YahooSummary()
        y['ticker'] = response.request.url[len(PREFIX + "/q?s="):]
        yield Request(PREFIX + "/q/ks?s=" + y['ticker'] + "+Key+Statistics", callback=self.serve(y))
        labels = []
        values = []
        if len(labels) != len(values):
            self.errors.append(y['ticker'] + " label value mismatch")
        for row in data:
            labels.append("".join(row.xpath('.//th//text()').extract()))
            values.append("".join(row.xpath('.//td//text()').extract()))
        for l, v in zip(labels, values):
            label = slugify(l)
            self.fields.add(label)
            try:
                y[label] = v
            except KeyError:
                self.errors.append(y['ticker'] + " label not found: " + label)

    def serve(self, y):
        """Curries to pass data"""
        def parse_key_stats(response):
            label_data = response.xpath('//*[@class="yfnc_tablehead1"]')
            value_data = response.xpath('//*[@class="yfnc_tabledata1"]')
            labels = []
            values = []
            for row in label_data:
                labels.append(slugify(row.xpath('.//text()').extract()[0]))
            for row in value_data:
                values.append(' '.join(row.xpath('.//text()').extract()))
            for l, v in zip(labels, values):
                self.fields.add(l)
                try:
                    y[l] = v
                except KeyError:
                    self.errors.append(y['ticker'] + " label not found: " + l)
            yield y
        return parse_key_stats

    def spider_closed(self, spider):
        print self.fields
        for f in self.fields:
            print f + " = scrapy.Field()"
        print "########## ERRORS ###########"
        for e in self.errors:
            print e
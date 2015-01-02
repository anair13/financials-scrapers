# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.shell import inspect_response
from finviz.items import YahooSummary, YahooKeyStats
import MySQLdb
import re
from unicodedata import normalize

# code adapted from http://stackoverflow.com/questions/9042515
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
def slugify(text, delim=u'_'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    # remove parens
    if '(' in text:
        i = text.index('(')
        text = text[:i]

    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    result = unicode(delim.join(result))
    if not result[0].isalpha(): # add _ if name starts with nu
        result = '_' + result
    return result

PREFIX = "http://finance.yahoo.com"

class YahooGeneralSpider(scrapy.Spider):
    name = "YahooGeneralSpider"
    allowed_domains = ["yahoo.com"]

    # get list of tickers
    DATABASE = ('192.168.1.117', 'scrn01', 'scrn01', 'scrn01')
    conn = MySQLdb.connect(*DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT `stocks`.`TICKER` FROM `scrn01`.`stocks`;')
    names = [i[0] for i in cur.fetchall() if len(i) > 0]

    start_urls = [PREFIX + "/q?s=" + ticker for ticker in names]

    def parse(self, response):
        """Parse the summary page"""
        # inspect_response(response)
        data = response.xpath('//*[@id="yfi_quote_summary_data"]/table/tr')
        y = YahooSummary()
        y['ticker'] = response.request.url[len(PREFIX + "/q?s="):]
        yield Request(PREFIX + "/q/ks?s=" + y['ticker'] + "+Key+Statistics", callback=self.parse_key_stats)
        labels = []
        values = []
        for row in data:
            labels.append("".join(row.xpath('.//th//text()').extract()))
            values.append("".join(row.xpath('.//td//text()').extract()))
        for l, v in zip(labels, values):
            y[slugify(l)] = v
        yield(y)

    def parse_key_stats(self, response):
        label_data = response.xpath('//*[@class="yfnc_tablehead1"]')
        value_data = response.xpath('//*[@class="yfnc_tabledata1"]')
        y = YahooKeyStats()
        y['ticker'] = response.request.url[len(PREFIX + "/q/ks?s="):-len("+Key+Statistics")]
        labels = []
        values = []
        for row in label_data:
            labels.append(slugify(' '.join(row.xpath('.//text()').extract())))
        for row in value_data:
            values.append(' '.join(row.xpath('.//text()').extract()))
        for l, v in zip(labels, values):
            y[l] = v
        yield y
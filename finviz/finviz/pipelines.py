# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from finviz.items import YahooSummary, YahooKeyStats


class FinvizPipeline(object):
    def process_item(self, item, spider):
        return item


class YahooExportPipeline(object):

    def __init__(self):
        self.keystat_file = open('yahoo_keystat.csv', 'w+b')
        self.summary_file = open('yahoo_summary.csv', 'w+b')
        self.summary_exporter = CsvItemExporter(self.summary_file)
        self.keystat_exporter = CsvItemExporter(self.keystat_file)
        self.summary_exporter.start_exporting()
        self.keystat_exporter.start_exporting()

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.summary_exporter.finish_exporting()
        self.keystat_exporter.finish_exporting()
        self.keystat_file.close()
        self.summary_file.close()

    def process_item(self, item, spider):
        if type(item) is YahooSummary:
            self.summary_exporter.export_item(item)
        if type(item) is YahooKeyStats:
            self.keystat_exporter.export_item(item)
        return item
# -*- coding: utf-8 -*-

# Scrapy settings for finviz project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'finviz'

SPIDER_MODULES = ['finviz.spiders']
NEWSPIDER_MODULE = 'finviz.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'finviz (+http://www.yourdomain.com)'

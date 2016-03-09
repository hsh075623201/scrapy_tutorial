# -*- coding: utf-8 -*-

import time
import json
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.settings import proxy_list
from news.utils import getItemColl
import re


class DmozSpider(MainSpider):
    name = "aastocks"
    allowed_domains = ["aastocks.com"]
    
    start_urls = [
        "http://www.aastocks.com/sc/stocks/news/aafn/latest-news"
    ]
    
    rules = [
        Rule(SgmlLinkExtractor(
            allow=(r'.*?/latest-news')), callback="parse_item"),
    ]

    def parse(self, response):
        urls = map(lambda x: "http://www.aastocks.com%s" % x, re.findall("/sc/stocks/news/aafn-content/NOW\.\d+?/latest-news", response.body))
        for url in urls:
            yield self.get_request(url)
    
    def parse_item(self, response):
        def set_help(item, key, xpath):
            try:
                item[key] = sel.xpath(xpath)[0].extract().encode("utf8")
            except:
                item[key] = ""
            
        sel = Selector(response)
        item = Item()

        # init item
        item["name"] = u"阿思達克财经"
        item["coll"] = getItemColl(self.name)
        item["host"] = "aastocks.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//p//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//span[@id='lblSTitle']//text()")

        return item

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
    name = "21jingji"
    allowed_domains = ["21jingji.com"]

    start_urls = [
        "http://m.21jingji.com/weixin/herald?from=timeline&isappinstalled=0"
    ]

    rules=[
        Rule(SgmlLinkExtractor(
            allow=(r'.*?article/\d+?/herald/.*?\.html')), callback="parse_item"),
    ]
    
    def parse_item(self, response):
        def set_help(item, key, xpath):
            try:
                item[key] = sel.xpath(xpath)[0].extract().encode("utf8")
            except:
                item[key] = ""
            
        sel = Selector(response)
        item = Item()

        # init item
        item["name"] = u"21经济"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.21jingji.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//div[@class='content']/section//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1//text()")

        return item
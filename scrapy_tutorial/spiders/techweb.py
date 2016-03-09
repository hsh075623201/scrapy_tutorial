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
    name = "techweb"
    allowed_domains = ["techweb.com.cn"]

    start_urls = [
        "http://www.techweb.com.cn/roll/"
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(
            allow=(r'/.*?/\d+?-\d+?-\d+?/\d+?\.shtml')), callback="parse_item"),
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
        item["name"] = u"techweb"
        item["coll"] = getItemColl(self.name)
        item["host"] = "techweb.com.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body/div[@class='main']/div[@class='left2']/div[@class='article']//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1//text()")

        return item
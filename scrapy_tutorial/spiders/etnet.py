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
    name = "etnet"
    allowed_domains = ["etnet.com.cn"]

    start_urls = [
        "http://news.etnet.com.cn/all"
    ]

    rules=[
        Rule(SgmlLinkExtractor(allow=(r'.*?\d+?\.htm')), callback="parse_item"),
    ]

    def parse(self, response):
        for url in re.findall(".*?(http://.*?\d+?\.htm).*?", response.body):
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
        item["name"] = u"经济通"
        item["coll"] = getItemColl(self.name)
        item["host"] = "etnet.com.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//div[@class='Newstextall']//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1//text()")

        return item

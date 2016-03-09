# -*- coding: utf-8 -*-

import random
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
    name = "p5w"
    allowed_domains = ["p5w.net"]

    start_urls = [
        "http://www.p5w.net/kuaixun/tj/"
    ]

    def parse(self, response):  
        prefix = "http://www.p5w.net/kuaixun/"
        for url in map(lambda x: "%s%s" % (prefix, x[3:]), re.findall(".*?(\.\./\d+?/t\d+?_\d+?\.htm).*?", response.body)):
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
        item["name"] = u"全景滚动"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.p5w.net"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//p//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//div[@class='title']//text()")

        return item

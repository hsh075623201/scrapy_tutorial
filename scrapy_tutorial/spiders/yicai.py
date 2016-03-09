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
    name = "yicai"
    allowed_domains = ["yicai.com"]
    date = int(time.time())*100
    start_urls = [
        "http://www.yicai.com/proxy/zxw_data.php?type=0&index=0&time=%s" % date
    ]

    def parse(self, response):  
        data = json.loads(response.body)
        for item in data["result"]:  
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
        item["name"] = u"一财网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.yicai.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//p//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1//text()")
        set_help(item, "source", "/html/body/div[@class='main']/div[@class='mainLeft']/div[@class='newList']/div[@class='content']/div[@class='info']/p[@id='source_baidu']//text()")

        return item

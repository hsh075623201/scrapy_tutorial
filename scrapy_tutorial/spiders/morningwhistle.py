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
    name = "morningwhistle"
    allowed_domains = ["morningwhistle.com"]

    start_urls = [
        "http://www.morningwhistle.com/website/login2Action!showList.action?news.type=2&news.toll=0"
    ]

    rules=[
        Rule(SgmlLinkExtractor(
            allow=(r'website/news/\d+?/\d+?\.html')), callback="parse_item"),
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
        item["name"] = u"晨哨网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.morningwhistle.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body/div[@class='con-w p-t-xxl']/div[@class='list-cont con-w m-t-md']/div[@class='list-l']/div[@class='cont-t']/div[@class='t-list']//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1//text()")

        try:
            update_time = sel.xpath("/html/body/div[@class='con-w p-t-xxl']/div[@class='list-cont con-w m-t-md']/div[@class='list-l']/div[@class='cont-t']/p[@class='msg']/span[3]//text()")[0].extract().encode("utf8")
            item["update_time"] = datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)
        
        return item
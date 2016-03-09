# -*- coding: utf-8 -*-

import random
from datetime import datetime
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.settings import proxy_list
from news.utils import getItemColl
import re


class DmozSpider(MainSpider):
    name = "money163"
    allowed_domains = ["money.163.com"]
    
    start_urls = [
        "http://money.163.com/special/00251G8F/news_json.js?%s" % random.random()
    ]

    def parse(self, response):
        for url in re.findall(".*?(http://money.*?html).*?", response.body):
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
        item["name"] = u"网易财经"
        item["coll"] = getItemColl(self.name)
        item["host"] = "money.163.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body/div[@id='js-epContent']/div[@class='ep-content-bg clearfix']/div[@id='epContentLeft']/div[@class='ep-main-bg']/div[@id='endText']//text()")])
        item["summary"] = ""
        item["author"] = ""

        set_help(item, "title", "/html/body/div[@id='js-epContent']/div[@class='ep-content-bg clearfix']/div[@id='epContentLeft']/div[@class='ep-main-bg']/h1[@id='h1title']//text()")

        return item


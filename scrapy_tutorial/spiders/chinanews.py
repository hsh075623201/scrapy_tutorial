# -*- coding: utf-8 -*-
import re
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.utils import getItemColl


class Spider(MainSpider):
    name = "chinanews"
    allowed_domains = ["finance.chinanews.com"]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=r'.*?\d+?\.shtml'), callback="parse_item")
    ]

    def start_requests(self):
        return [Request("http://finance.chinanews.com/cj/gd.shtml", headers={"Upgrade-Insecure-Requests:":"1", "Host" :"finance.chinanews.com"})]
    
    def parse(self, response):
        for url in map(lambda x: "http://finance.chinanews.com%s" % x, re.findall(".*?(/cj/\d+?/\d+?-\d+?/\d+?\.shtml).*?", response.body)):
            yield self.get_request(url)

    def parse_item(self, response):
        def set_help(item, key, xpath):
            try:
                item[key] = sel.xpath(xpath)[0].extract().encode("utf-8")
            except:
                item[key] = ""

        sel = Selector(response)
        item = Item()
        # init item
        item["name"] = u"中新网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "chinanews.com"
        item["link"] = response.url

        item["content"] = "<br />".join([n.extract().encode("utf-8") for n in sel.xpath("//div[@id='cont_1_1_2']//text()")])
        item["summary"] = ""

        item["source"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1//text()")

        return item

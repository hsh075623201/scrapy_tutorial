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
from news.settings import proxy_list
from news.utils import getItemColl


class Spider(MainSpider):
    name = "cnstock"
    allowed_domains = ["cnstock.com"]
    start_urls = [
        "http://news.cnstock.com/bwsd"
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=r'.*?\d+?\.htm'), callback="parse_item")
    ]

    def parse(self, response):
        for url in re.findall(".*?(http://.*?/\d+?\.htm).*?", response.body):
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
        item["name"] = u"中国证券网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "news.cnstock.com"
        item["link"] = response.url

        item["content"] = "<br />".join([n.extract().encode("utf-8") for n in sel.xpath("//div[@id='qmt_content_div']//text()")])
        item["summary"] = ""

        item["source"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1//text()")

        return item

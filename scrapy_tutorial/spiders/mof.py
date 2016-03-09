# -*- coding: utf-8 -*-

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
    name = "mof"
    allowed_domains = ["mof.gov.cn"]
    start_urls = [
        "http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/"
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=(r".*?guizhangzhidu/\d+?/.*?\.html")), callback="parse_item"),
    ]

    def parse(self, response):
        for url in re.findall(".*?(http://.*?/t\d+?_\d+?\.html).*?", response.body):
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
        item["name"] = u"财政部"
        item["coll"] = getItemColl(self.name)
        item["host"] = "mof.gov.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//td//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//td[@id='Zoom']//text()")
        if len(item["title"].strip()) < 2:
            set_help(item, "title", "//td[@class='font_biao1']//text()")

        item["source"] = ""

        return item

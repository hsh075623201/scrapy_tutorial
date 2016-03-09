# -*- coding: utf-8 -*-

from datetime import datetime
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
    name = "ndrc"
    allowed_domains = ["www.ndrc.gov.cn"]
    start_urls = [
        "http://www.ndrc.gov.cn/xwzx/xwfb/"
    ]

    rules=[
        Rule(SgmlLinkExtractor(allow=(r"http://www.ndrc.gov.cn/xwzx/xwfb/\d+?/t\d+?_\d+?\.html")), callback="parse_item"),
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
        item["name"] = u"发改委"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.ndrc.gov.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body[@class='body_bg1']/div[@id='wrapper']/div[@id='out-content']/div[@class='index_wrapper1 screen_width clearfix']/div[@class='Middle4']/div[@class='Middle4_body']/div[@id='zoom']/div[@class='TRS_Editor']/p//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body[@class='body_bg1']/div[@id='wrapper']/div[@id='out-content']/div[@class='index_wrapper1 screen_width clearfix']/div[@class='Middle4']/div[@class='Middle4_body']/div[@id='zoom']/div[@class='TRS_Editor']/p[1]/font//text()")

        return item
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
    name = "miit"
    allowed_domains = ["miit.gov.cn"]
    start_urls = [
        "http://www.miit.gov.cn/newweb/n1146295/n1652858/n1653100/index.html",
        "http://www.miit.gov.cn/newweb/n1146295/n1652858/n1652930/index.html"
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=(r".*?content\.html")), callback="parse_item"),
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
        item["name"] = u"工信部"
        item["coll"] = getItemColl(self.name)
        item["host"] = "miit.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body/div[@class='w980 center cmain']/div[@id='con_con']//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body/div[@class='w980 center cmain']/div[@class='ctitle']/h1[@id='con_title']//text()")
        set_help(item, "source", "//div[@id='artInfo']/a/text()")

        try:
            update_time = sel.xpath("/html/body/div[@class='w980 center cmain']/div[@class='cinfo center']/span[@id='con_time']//text()")[0].extract().encode("utf8")[15:]
            item["update_time"] = datetime.strptime(update_time, "%Y-%m-%d")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)
        return item
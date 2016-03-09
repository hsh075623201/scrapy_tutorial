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
    name = "pbc"
    allowed_domains = ["pbc.gov.cn"]
    
    start_urls = [
        "http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html"
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'.*?\d+?/\d+?/\d+?/index\.html')), callback="parse_item"),
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
        item["name"] = u"央行发布"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.pbc.gov.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body/div[@class='mainw950']/div[@id='pre']/div[@id='10929']/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body/div[@class='mainw950']/div[@id='pre']/div[@id='10929']/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr/td/h2//text()")
        set_help(item, "source", "/html/body/div[@class='mainw950']/div[@id='pre']/div[@id='10929']/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td[@class='hui12'][2]/span[@id='laiyuan']//text()")

        try:            
            update_time=sel.xpath("/html/body/div[@class='mainw950']/div[@id='pre']/div[@id='10929']/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td[@class='hui12'][3]//text()")[1].extract().encode("utf8")
            item["update_time"] = datetime.strptime(update_time.strip(), "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)

        return item
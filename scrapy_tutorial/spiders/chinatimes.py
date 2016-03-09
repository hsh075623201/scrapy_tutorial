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
    name = "chinatimes"
    allowed_domains = ["chinatimes.cc"]
    
    start_urls = [
        "http://www.chinatimes.cc/finance"
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'.*?article/\d+?\.html')), callback="parse_item"),
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
        item["name"] = u"华夏时报网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.chinatimes.cc"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body/div[@class='main']/div[@class='mainLeft']/div[@class='newList']/div[@class='content']/div[@class='infoMain']//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1//text()")
        set_help(item, "source", "/html/body/div[@class='main']/div[@class='mainLeft']/div[@class='newList']/div[@class='content']/div[@class='info']/p[@id='source_baidu']//text()")

        try:
            pattern=re.compile(".*?(\d+?-\d+?-\d+?.*?\d+?:\d+?:\d+).*")
            update_time = sel.xpath("/html/body/div[@class='main']/div[@class='mainLeft']/div[@class='newList']/div[@class='content']/div[@class='info']//text()")[7].extract().encode("utf8")
            match=pattern.search(update_time)            
            item["update_time"] = datetime.strptime(match.groups()[0], "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)

        return item
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
    name = "caixin"
    allowed_domains = ["caixin.com"]
    start_urls = [
        "http://www.caixin.com/search/scroll/index.jsp",
        "http://economy.caixin.com/",
        "http://finance.caixin.com/",
        "http://companies.caixin.com/",
    ]

    rules=[
        Rule(SgmlLinkExtractor(allow=(r'http://.*?\.caixin.com/\d+?-\d+?-\d+?/\d+?\.html')), callback="parse_item"),
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
        item["name"] = u"财新网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "caixin.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//div[@id='Main_Content_Val']//p/text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "//h1/text()")
        set_help(item, "source", "//div[@id='artInfo']/a/text()")

        try:            
            pattern=re.compile(".*(\d{4}).*(\d{2}).*(\d{2}).*(\d{2}):(\d{2}).*")
            update_time=sel.xpath("//div[@id='artInfo']//text()")[0].extract().encode("utf8")
            match=pattern.search(update_time)
            item["update_time"] = datetime.strptime(match.group().strip()[0:23], "%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)
        return item
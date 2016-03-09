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
    name = "zhongxin"
    allowed_domains = ["finance.chinanews.com"]
    start_urls = [
        "http://finance.chinanews.com/cj/gd.shtml",
    ]
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'http://finance.chinanews.com/cj/\d+?/\d+?-\d+?/\d+?\.shtml')), callback="parse_item"),
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
        item["name"] = u"中新网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "finance.chinanews.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//div[@id='cont_1_1_2']")])
        item["summary"] = ""
        item["author"] = ""
        #set_help(item, "author", "//span[@id='author_baidu']/text()")
        set_help(item, "title", "//*[@id='cont_1_1_2']/h1/text()")
        set_help(item, "source", "/div[@id='cont_1_1_2']/div[@class='left-time']/div[@class='left-t']/a[1]//text()")

        try:
            pattern=re.compile(".*(\d{4}).*(\d{2}).*(\d{2}).*(\d{2}):(\d{2}).*")
            update_time=sel.xpath('//*[@id="cont_1_1_2"]/div[4]/div[2]/text()')[0].extract().encode("utf8")
            match=pattern.search(update_time)
            item["update_time"] = datetime.strptime(match.group()[1:24], "%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)

        return item


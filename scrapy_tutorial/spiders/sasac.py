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
    name = "sasac"
    allowed_domains = ["www.sasac.gov.cn"]
    start_urls = [
        "http://www.sasac.gov.cn/n85881/n85901/index.html",
        "http://www.sasac.gov.cn/n86302/n86376/index.html"
    ]

    rules=[
        Rule(SgmlLinkExtractor(allow=(r"http://www.sasac.gov.cn/n\d+?/n\d+?/c\d+?/content.html")), callback="parse_item"),
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
        item["name"] = u"国资委"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.sasac.gov.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body/div[@class='main center']/div[@id='con_con']//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body/div[@class='main center']/div[@class='ttitle']/h1[@id='con_title']//text()")
        set_help(item, "source", "/html/body/div[@class='main center']/div[@class='tinfo relative']/span[@id='con_ly']//text()")

        try:            
            update_time = sel.xpath("/html/body/div[@class='main center']/div[@class='tinfo relative']/span[@id='con_time']//text()")[0].extract().encode("utf8")
            item["update_time"] = datetime.strptime(update_time.strip(), "%Y-%m-%d")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)
        return item
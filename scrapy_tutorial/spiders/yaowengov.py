# -*- coding: utf-8 -*-
import re
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.settings import proxy_list
from news.utils import getItemColl


class Spider(MainSpider):
    name = "yaowengov"
    allowed_domains = ["www.gov.cn"]
    start_urls = [
        "http://www.gov.cn/xinwen/yaowen.htm"
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=r'\d+?-\d+?/\d+?/content_\d+?\.htm'), callback="parse_item")
    ]

    def parse_item(self, response):
        def set_help(item, key, xpath):
            try:
                item[key] = sel.xpath(xpath)[0].extract().encode("utf-8")
            except:
                item[key] = ""

        sel = Selector(response)
        item = Item()

        # init item
        item["name"] = u"中国政府网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.gov.cn"
        item["link"] = response.url

        item["content"] = "<br />".join([n.extract().encode("utf-8") for n in sel.xpath("/html/body[@class='body_bg']/div[@class='wrap']/div[@class='frame-pane']/div[@class='article-colum']/div[@id='UCAP-CONTENT']/table[@id='printContent']//text()")])
        item["summary"] = ""

        item["source"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body[@class='body_bg']/div[@class='wrap']/div[@class='frame-pane']/div[@class='article-colum']/div[@class='pages-title']//text()")

        return item
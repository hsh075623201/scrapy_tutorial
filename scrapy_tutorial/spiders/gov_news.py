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
    name = "govnews"
    allowed_domains = ["gov.cn"]
    
    start_urls = [
        "http://www.gov.cn/xinwen/xw_bmxw.htm",
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'.*?\d+?-\d+?/\d+?/content_\d+?\.htm')), callback="parse_item"),
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
        item["name"] = u"中国政府网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.gov.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body[@class='body_bg']/div[@class='wrap']/div[@class='frame-pane']/div[@class='article-colum']/div[@id='UCAP-CONTENT']/table[@id='printContent']//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body[@class='body_bg']/div[@class='wrap']/div[@class='frame-pane']/div[@class='article-colum']/div[@class='pages-title']//text()")
        set_help(item, "source", "/html/body[@class='body_bg']/div[@class='wrap']/div[@class='frame-pane']/div[@class='article-colum']/div[@class='pages-date']/span[@class='font'][2]//text()")

        
        return item
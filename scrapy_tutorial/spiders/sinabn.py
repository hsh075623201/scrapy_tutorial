# -*- coding: utf-8 -*-

import md5
from datetime import datetime
from scrapy.http import Request, TextResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.settings import proxy_list
from news.utils import getItemColl
import re
from BeautifulSoup import BeautifulSoup
from scrapy.utils.spider import iterate_spider_output


class DmozSpider(MainSpider):
    name = "bnsina"
    allowed_domains = ["bn.sina.cn"]
    
    start_urls = [
        "http://bn.sina.cn/video/live?channel=finance&newsid=globalnews1&vt=4&live_mg=sports"
    ]

    def parse(self, response):
        b = BeautifulSoup(response.body)
        details = b.findAll(attrs={"class": "detail"})
        
        for detail in details:
            resp = TextResponse(url="..", status=200, body=detail.text.encode("utf8"))
            for requests_or_item in iterate_spider_output(self.parse_item(resp)):
                yield requests_or_item

    def parse_item(self, response):
        def set_help(item, key, xpath):
            try:
                item[key] = sel.xpath(xpath)[0].extract().encode("utf8")
            except:
                item[key] = ""
            
        sel = Selector(response)
        item = Item()

        # init item
        item["name"] = u"新浪财经"
        item["coll"] = getItemColl(self.name)
        item["host"] = "bn.sina.cn"
        item["link"] = "bnsina%s" % md5.md5(response.body).hexdigest()
        item["content"] = response.body
        item["summary"] = ""
        item["author"] = ""
        item["title"] = response.body.decode("utf8")[:20].encode("utf8")

        return item

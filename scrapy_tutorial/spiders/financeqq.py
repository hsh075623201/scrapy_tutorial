# -*- coding: utf-8 -*-

import random
from datetime import datetime
from scrapy.http import Request
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
    name = "financeqq"
    allowed_domains = ["finance.qq.com"]

    def start_requests(self):
        return [Request("http://roll.finance.qq.com/interface/roll.php?%s&cata=&site=finance&date=&page=1&mode=1&of=json" % random.random(), headers={"Referer":"http://roll.finance.qq.com"})]

    def parse(self, response):
        urls = map(
            lambda x:x.replace("\\", ""),
            re.findall("http:.*?\.htm",
                       eval(response.body, {}, {})["data"]["article_info"]))        

        for url in urls:
            yield self.get_request(url)

    def parse_item(self, response):
        def set_help(item, key, xpath):
            try:
                item[key] = sel.xpath(xpath)[0].extract().encode("utf8")
            except:
                item[key] = ""
            
        sel = Selector(response)
        item = Item()

        # init item
        item["name"] = u"腾讯财经"
        item["coll"] = getItemColl(self.name)
        item["host"] = "finance.qq.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body[@id='Wrap']/div[@class='body-Article-QQ']/div[@id='Main-Article-QQ']/div[@id='MainL']/div[@class='main']/div[@id='C-Main-Article-QQ']/div[@class='bd']/div[@id='Cnt-Main-Article-QQ']//text()")])
        item["summary"] = ""
        item["author"] = ""

        set_help(item, "title", "//h1//text()")

        return item


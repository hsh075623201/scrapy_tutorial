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
    name = "zhongzheng"
    allowed_domains = ["news.cnstock.com"]
    start_urls = [
        "http://news.cnstock.com/bwsd",
    ]

    rules=[        
        Rule(SgmlLinkExtractor(allow=(r'http://news.cnstock.com/news/sns_bwkx/\d+?/\d+?\.htm')), callback="parse_item"),
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
        item["name"] = u"上证快讯"
        item["coll"] = getItemColl(self.name)
        item["host"] = "news.cnstock.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//p")])
        item["summary"] = ""
        item["author"] = ""
        #set_help(item, "author", "//span[@id='author_baidu']/text()")
        set_help(item, "title", "//*[@id='pager-content']/h1/text()")
        set_help(item, "source", "//*[@id='pager-content']/div[1]/span[2]/a/text()")
        try:
            pattern=re.compile("(\d{4})-(\d{2})-(\d{2}).*(\d{2}):(\d{2}):\d{2}")
            update_time=sel.xpath('//*[@id="pager-content"]/div[1]/span[1]/text()')[0].extract()
            match=pattern.search(update_time)
            item["update_time"] = datetime.strptime(match.group(), "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            raise DropItem(str(e))

        return item


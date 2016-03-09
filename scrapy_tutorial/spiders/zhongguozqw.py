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
    name = "zhongguozqw"
    allowed_domains = ["ggjd.cnstock.com"]
    start_urls = [
        "http://ggjd.cnstock.com/gglist/search/ggkx",
    ]
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'http://ggjd.cnstock.com/company/scp_ggjd/tjd_ggkx/\d+?/\d+?\.htm')), callback="parse_item"),
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
        item["name"] = u"中国证券网-上市公司公告快讯"
        item["coll"] = getItemColl(self.name)
        item["host"] = "ggjd.cnstock.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//p")])
        item["summary"] = ""
        set_help(item, "author", "//*[@id='pager-content']/div[1]/span[3]/text()")
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


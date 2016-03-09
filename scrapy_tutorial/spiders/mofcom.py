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
    name = "mofcom"
    allowed_domains = ["www.mofcom.gov.cn"]
    start_urls = [
        "http://www.mofcom.gov.cn/article/ae/ai/",
    ]

    rules=[
        Rule(SgmlLinkExtractor(allow=(r"http://.*?mofcom\.gov\.cn/article/ae/ai/\d+?/\d+?\.shtml")), callback="parse_item"),
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
        item["name"] = u"商务部日常新闻"
        item["coll"] = getItemColl(self.name)
        item["host"] = "mofcom.gov.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body/div[@id='wrap']/div[@class='MainList']/div[@class='article_new mt10']/div[@id='zoom']//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body/div[@id='wrap']/div[@class='MainList']/div[@class='article_new mt10']/h4[@id='artitle']//text()")
        set_help(item, "source", "/html/body/div[@id='wrap']/div[@class='MainList']/div[@class='article_new mt10']/div[@id='arsource']/a//text()")

        try:
            item["update_time"] = datetime.strptime(re.search('var tm = \"(.*?)\"', response.body).groups()[0], "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)
        return item
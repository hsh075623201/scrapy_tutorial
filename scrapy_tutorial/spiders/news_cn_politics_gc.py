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


class DmozSpider(MainSpider):
    name = "news_cn_politics"
    allowed_domains = ["www.news.cn","news.xinhuanet.com"]
    start_urls = [
        "http://www.news.cn/politics/leaders/gdxw.htm"
    ]
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'http://news.xinhuanet.com/politics/\d+?-\d+?/\d+?/\w+?.htm')), callback="parse_item"),
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
        item["name"] = u"新华网-高层"
        item["coll"] = getItemColl(self.name)
        item["host"] = "news.xinhuanet.com/gc"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//*[@id='content']//p")])
        if not item["content"]:
            item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//div[@class='article']//text()")])

        try:
            update_time = sel.xpath("//*[@id='article']//*[@class='time']//text()")[0].extract().encode("utf8").strip()
            item["update_time"] = datetime.strptime(update_time, "%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M:%S")
        except Exception as e:
            pass

	item["summary"] = ""
        item['author'] = ""
        set_help(item, "title", "//*[@id='title']/text()")
        set_help(item, "source", "//*[@id='source']/text()")
	
        return item

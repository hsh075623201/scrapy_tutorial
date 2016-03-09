# -*- coding: utf-8 -*-

import re
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors import LinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.settings import proxy_list
from news.utils import getItemColl


class DmozSpider(MainSpider):
    name = "news_cn_cjlb"
    allowed_domains = ["www.news.cn","news.xinhuanet.com", "203.192.8.57"]
    start_urls = [
        #"http://www.news.cn/fortune/cjlblist.htm",
        "http://203.192.8.57/was5/web/search?channelid=214510&prepage=25&searchword=extend5%3D%27%25115033%25%27"
    ]
    # rules=[
    #     # Rule(LinkExtractor(allow=(r'http://news.xinhuanet.com/fortune/\d+?-\d+?/\d+?/\w+?.htm')), callback="parse_item"),
    #     Rule(LinkExtractor(allow=(r'http://.*c_\d+?\.htm')), callback="parse_item"),
    # ]

    def parse(self, response):
        # import ipdb;ipdb.set_trace()
        for url in re.findall(".*?(http://.*c_\d+?\.htm).*?", response.body):
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
        item["name"] = u"新华网财经联播"
        item["coll"] = getItemColl(self.name)
        item["host"] = "news.xinhuanet.com"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//p//text()")])


	item["summary"] = ""
        item['author'] = ""
        set_help(item, "title", "//h1//text()")
	
        return item

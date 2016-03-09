# -*- coding: utf-8 -*-

import json
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
    name = "sina_usstock"
    allowed_domains = ["finance.sina.com.cn"]
    date = datetime.now().strftime("%Y%m%d")
    start_urls = [
        "http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=cjxwpl&top_time=%s&top_show_num=50&top_order=DESC&js_var=all_1_data" % date,
    ]

    def parse(self, response):  
        data = json.loads(response.body[17:-2])
        for item in data["data"]:  
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
        item["name"] = u"新浪财经-产经滚动"
        item["coll"] = getItemColl(self.name)
        item["host"] = "finance.sina.com.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//p")])
        item["summary"] = ""
        item["author"] = ""
        #set_help(item, "author", "//span[@id='author_baidu']/text()")
        set_help(item, "title", "h1[@id='artibodyTitle']//text()")
        set_help(item, "source", "/div[@class='page-info']/span[@class='time-source']/span/a//text()")
        try:
            update_time = sel.xpath("//span[@class='time-source']//text()")[0].extract().encode("utf8")
            item["update_time"] = datetime.strptime(update_time[:25], "\n%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5\xc2\xa0%H:%M")
        except Exception as e:
            print str(e)
            return None

        return item


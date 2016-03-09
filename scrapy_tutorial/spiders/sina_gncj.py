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
    name = "sina_gncj"
    allowed_domains = ["finance.sina.com.cn"]
    start_urls = [
        "http://roll.finance.sina.com.cn/finance/gncj/gncj/index.shtml",
    ]
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'http://finance.sina.com.cn/china/\d+?/\d+?\.shtml')), callback="parse_item"),
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
        item["name"] = u"新浪财经-国内财经"
        item["coll"] = getItemColl(self.name)
        item["host"] = "finance.sina.com.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//*[@id='artibody']/p")])
        try:
            update_time = sel.xpath("//*[@id='wrapOuter']//*[@class='time-source']/text()")[0].extract().encode("utf8").strip()
            item["update_time"] = datetime.strptime(update_time, "%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5\xc2\xa0%H:%M")
        except Exception as e:
            pass

        item["summary"] = ""
        item['author'] = ""
        set_help(item, "title", "//*[@id='artibodyTitle']/text()")
        set_help(item, "source", "//*[@data-sudaclick='media_name']/text()")

        return item

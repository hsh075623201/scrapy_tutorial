# -*- coding: utf-8 -*-
import re
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.settings import proxy_list
from news.utils import getItemColl


class CsrcSpider(MainSpider):
    name = "csrc"
    allowed_domains = ["csrc.gov.cn"]
    start_urls = [
        "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/"
    ]
    # rules=[
    #     # http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/201511/t20151113_286557.html
    #     # www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/\d+?/.*\.html
    #     Rule(SgmlLinkExtractor(
    #         allow=(r'.*?t\d+?_\d+?\.html')),
    #         callback="parse_item"
    #     ),
    # ]

    def parse(self, response):
        
        prefix = "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd"
        urls = map(lambda x: "%s%s" % (prefix, x[1:]), re.findall("\./\d+?/t\d+?_\d+?\.html", response.body))
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
        item["name"] = u"证监会要闻"
        item["coll"] = getItemColl(self.name)
        item["host"] = "csrc.gov.cn"
        item["link"] = response.url
        
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//p//text()")])

        set_help(item, "title", "//div[@class='title']/text()")
        print item["title"], item["link"]

        return item


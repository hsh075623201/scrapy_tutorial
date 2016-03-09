# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.settings import proxy_list
from news.utils import getItemColl
import re


class DmozSpider(MainSpider):
    name = "hangyunjie"
    allowed_domains = ["www.ship.sh", "ship.sh"]
    start_urls = [
        "http://www.ship.sh/info.php",
    ]

    rules=[
        Rule(SgmlLinkExtractor(allow=(r'.*?nid=\d+')), callback="parse_item"),
    ]

    def parse(self, response):
        urls = map(lambda x: "http://www.ship.sh%s" % x[1:], re.findall("\./news_detail\.php\?nid=\d+", response.body))
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
        dateNow=datetime.now().year

        # init item
        item["name"] = u"航运界"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.ship.sh"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//text()")])
        item["summary"] = ""
        item["author"] = ""
        #set_help(item, "author", "//span[@id='author_baidu']/text()")
        set_help(item, "title", "//h1//text()")

        return item


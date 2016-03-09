# -*- coding: utf-8 -*-
import re
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from news.items import Item
from news.spider import MainSpider
from news.settings import proxy_list
from news.utils import getItemColl


class KuaixunSpider(MainSpider):
    name = "kuaixun"
    allowed_domains = ["kuaixun.stcn.com"]
    start_urls = [
        "http://kuaixun.stcn.com/"
    ]
    rules=[
        # http://kuaixun.stcn.com/2015/1130/12494840.shtml
        # http://kuaixun.stcn.com/\d+/\d+/\d+\.shtml
        Rule(
            SgmlLinkExtractor(
                allow=r'http://kuaixun.stcn.com/\d+/\d+/\d+\.shtml'
            ),
            callback="parse_item"
        )
    ]

    def parse_item(self, response):
        def set_help(item, key, xpath):
            try:
                item[key] = sel.xpath(xpath)[0].extract().encode("utf-8")
            except:
                item[key] = ""

        sel = Selector(response)
        item = Item()

        # init item
        item["name"] = u"证券时报"
        item["coll"] = getItemColl(self.name)
        item["host"] = "kuaixun.stcn.com"
        item["link"] = response.url

        item["content"] = "<br />".join([n.extract().encode("utf-8") for n in sel.xpath("//p")])
        item["summary"] = ""

        item["source"] = sel.xpath("//div[@class='intal_tit']/div[@class='info']/text()")[0].extract().encode("utf-8").split("\xef\xbc\x9a")[1]
        item["author"] = ""
        set_help(item, "title", "//div[@class='intal_tit']/h2/text()")
        try:
            pattern = re.compile(".*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})")
            update_time = sel.xpath("//div[@class='intal_tit']/div[@class='info']/text()")[0].extract()
            match = pattern.search(update_time)
            item["update_time"] = datetime.strptime(
                match.group(1),
                "%Y-%m-%d %H:%M"
            )
        except Exception as e:
            raise DropItem("get update_time failed")

        return item


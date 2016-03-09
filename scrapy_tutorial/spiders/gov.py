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
    name = "gov"
    allowed_domains = ["gov.cn"]
    
    start_urls = [
        "http://new.sousuo.gov.cn/list.htm?sort=pubtime&advance=true&t=paper&n=15",
    ]
    
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'.*?\d+?-\d+?/\d+?/content_\d+?\.htm')), callback="parse_item"),
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
        item["name"] = u"中国政府网"
        item["coll"] = getItemColl(self.name)
        item["host"] = "www.gov.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("/html/body[@class='body_bg']/div[@class='wrap']/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[@class='b12c']/p[2]//text()")])
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body[@class='body_bg']/div[@class='wrap']/table[1]/tbody/tr/td/table[@class='bd1'][1]/tbody/tr[3]/td[2]//text()")
        set_help(item, "source", "/html/body[@class='body_bg']/div[@class='wrap']/table[1]/tbody/tr/td/table[@class='bd1'][1]/tbody/tr[2]/td[2]//text()")

        try:            
            update_time=sel.xpath("/html/body[@class='body_bg']/div[@class='wrap']/table[1]/tbody/tr/td/table[@class='bd1'][1]/tbody/tr[4]/td[4]//text()")[0].extract().encode("utf8")
            item["update_time"] = datetime.strptime(update_time, "%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5")
        except Exception as e:
            raise DropItem("get update_time failed, %s" % e)
        return item
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
    name = "lwn"
    allowed_domains = ["lwn.net"]
    start_urls = [
        "http://lwn.net/Kernel/Index",
    ]

    rules=[        
        Rule(SgmlLinkExtractor(allow=(r'/Articles/\d+?/')), callback="parse_item"),
    ]

    def parse_item(self, response):
        print "parse_item***********************"
        def set_help(item, key, xpath):
            try:
                item[key] = sel.xpath(xpath)[0].extract().encode("utf8")
            except:
                item[key] = ""
            
        sel = Selector(response)
        item = Item()

        # init item
        item["name"] = "lwn"
        item["coll"] = getItemColl(self.name)
        item["host"] = "lwn.net"
        item["link"] = response.url
        #item["content"] = "content"
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//div[@class='ArticleText']")])
        item["summary"] = ""
        item["author"] = "author"
        #set_help(item, "author", "//span[@id='author_baidu']/text()")
        set_help(item, "title", "//head/title/text()")
        #item["title"] = "title"
        item["source"] = ""
        #set_help(item, "source", "//*[@id='pager-content']/div[1]/span[2]/a/text()")
        try:
            # pattern=re.compile("(\d{4})-(\d{2})-(\d{2}).*(\d{2}):(\d{2}):\d{2}")
            # update_time=sel.xpath('//div[@class="Byline"]/div[1]/span[1]/text()')[0].extract()
            # match=pattern.search(update_time)
            #item["update_time"] = datetime.strptime(match.group(), "%Y-%m-%d %H:%M:%S")
            item["update_time"] = "2016-01-01 00:00:00"
        except Exception as e:
            raise DropItem(str(e))
        print item
        
        return item


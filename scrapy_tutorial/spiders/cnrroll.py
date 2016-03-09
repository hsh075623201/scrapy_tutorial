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


class CnrRollSpider(MainSpider):
    name = "cnrroll"
    
    allowed_domains = ["www.cnr.cn"]
    
    # 种子(新闻列表页的url)
    start_urls = [
        "http://roll.cnr.cn/finance/",
    ]
    # a http://www.taizhou.com.cn/news/2015-11/30/content_2596111.htm
    # b http://www.taizhou.com.cn/news/\d+?-\d+?/\d+?/content_\d+?\.htm    
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'http://www.cnr.cn/list/finance/\d+?/t\d+?_\d+?\.shtml')), callback="parse_item",),
        Rule(SgmlLinkExtractor(allow=(r'http://www.cnr.cn/jingji/gundong/\d+?/t\d+?_\d+?\.shtml')), callback="parse_item"),
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
        item["name"] = u"央广网-经济之声"
        item["coll"] = getItemColl(self.name) # mongodb collection name
        item["host"] = "www.cnr.cn"
        item["link"] = response.url
        item["content"] = "<br />".join([n.extract().encode("utf8") for n in sel.xpath("//div[@class='TRS_Editor']")])
        # summary 可以不要
        item["summary"] = ""
        item["author"] = ""
        set_help(item, "title", "/html/body/div[@id='Area']/div[@id='cntl']/div[@class='wh645 left']/p[@class='f22 lh30 yahei']//text()")
        # source 可以不要
        set_help(item, "source", "/html/body/div[@id='Area']/div[@id='cntl']/div[@class='wh645 left']/p[@class='lh30 left f14 yahei']/a//text()")

        try:
            item["update_time"] = datetime.strptime(
                sel.xpath("/html/body/div[@id='Area']/div[@id='cntl']/div[@class='wh645 left']/p[@class='lh30 left f14 yahei']//text()")[0].extract().encode("utf8")[:19],
                "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print "get update_time failed, error:%s" % e
            return None            
        
        return item

# -*- coding: utf-8 -*-

import random
from datetime import datetime
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
import redis
from news.items import Item
from news.settings import proxy_list
from news.utils import getItemColl


class MainSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        CrawlSpider.__init__(self, *args, **kwargs)
        self.proxy_pool = proxy_list

    def parse(self, response):
        for res in CrawlSpider.parse(self, response):
            yield self.get_request(res.url)

    def get_request(self, url):
        r = redis.Redis()
        if r.get("url:%s" % url):
            return None
        else:
            if url not in self.start_urls:
                r.set(name="url:%s" % url, value="1", ex=60*60)
            
            req = Request(url, self.parse_item)
            if self.proxy_pool:
                proxy_addr = self.proxy_pool[random.randint(0, len(self.proxy_pool) - 1)]
                req.meta['proxy'] = "http://%s:%s" % (proxy_addr[0], proxy_addr[1])
            return req

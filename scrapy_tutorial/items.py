import scrapy

class Item(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    host = scrapy.Field()
    update_time = scrapy.Field()
    coll = scrapy.Field()

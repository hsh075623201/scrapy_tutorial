import datetime
import pymongo

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        print "init..."
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        print "from_crawler...."
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'content')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):        
        self.db["items"].create_index("link", unique=True)
        dicted_item = dict(item)
        try:
            if dicted_item["update_time"]:
                dicted_item["update_time"] = dicted_item["update_time"] - datetime.timedelta(hours=8)
        except Exception as e:
            pass
            
        dicted_item["insert_time"] = datetime.datetime.utcnow()
        if dicted_item["content"] == "":
            return None

        try:
            self.db["items"].insert(dicted_item)
        except Exception as e:
            return None
            
        return item

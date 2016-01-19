# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

# get properties' value from the settings.py file
from scrapy.conf import settings

from scrapy.exceptions import DropItem
from scrapy import log

class MongoDBPipeline(object):

    def __init__(self):
        
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    # when the spider yields the item, below function will be triggered     
    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        
        # it will either insert or update data that your spider yields with
        # appoint item as its dictionary
        # when upsert value is true, then it will also do save besides update 
        self.collection.update(
            {'store_name': item['name'], 
            'dong_val': item['link']}, 
            dict(item), 
            upsert=True)
        # you can log things you like
        log.msg("data added to database!", level=log.DEBUG, spider=spider)
        
        return item
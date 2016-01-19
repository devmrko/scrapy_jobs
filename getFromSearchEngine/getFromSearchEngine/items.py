# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

# put name of data models you want(e.g. name of mongoDB document's  entries)
class GetFromSearchEngineItem(Item):
    name = Field()
    link = Field()
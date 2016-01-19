# -*- coding: utf-8 -*-

BOT_NAME 			= 'getFromSearchEngine'
SPIDER_MODULES 		= ['getFromSearchEngine.spiders']
NEWSPIDER_MODULE 	= 'getFromSearchEngine.spiders'
ITEM_PIPELINES 		= {'getFromSearchEngine.pipelines.MongoDBPipeline': 1000, }

DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
	'getFromSearchEngine.rotate_useragent.RotateUserAgentMiddleware' :400
}

# put your mongoDB's account info
MONGODB_SERVER	= ""
MONGODB_PORT = 27017
MONGODB_DB 	= ""
MONGODB_COLLECTION 	= "
DOWNLOAD_DELAY = 30
CONCURRENT_REQUESTS = 1
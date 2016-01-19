# -*- coding: utf-8 -*-

import scrapy
import urllib

# change encoding to utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.closespider import CloseSpider

from pymongo import MongoClient
# selenium is an open-source project of the firefox web-browser
from selenium import webdriver

# include the pyhon item file to yield with
from getFromSearchEngine.items import GetFromSearchEngineItem

class getFromSearchEngineSpider(CrawlSpider):

    def __init__(self, *args, **kwargs):
        # URL address that your spider crawl in, and I add a query prameter to use search engine 
        # curUrl is the web search page that your crawler working at
        self.curUrl = ''

        # 'p_args' refers an identifier of arguments
        if(kwargs.get('p_args') == None):
            self.error_code = 1;
        else:
            self.error_code = 0;
            # make url with several parameters from command line
            self.parameter = kwargs.get('p_args')
            self.curUrl = self.curUrl + '""' + kwargs.get('p_args') + '"'
            print ">>>>> url: ", self.curUrl
            # initialize web browser 
            self.driver = webdriver.Firefox()
            self.start_urls = [self.curUrl]

        super(getFromSearchEngineSpider, self).__init__(*args, **kwargs)

    name = 'getFromSearchEngine'

    def parse(self, response):

        print ">>>>> parse start"

        if(self.error_code == 1):
            print ">>>>> error:", 'one of mandatory arguments is not retrieved'
            raise CloseSpider()

        # run selenium with the url
        self.driver.get(response.url)

        # this example is for the mobile site which has a pagination function working as appending next page_source
        # when you click next button or sort of things
        while True:
            try:
                # you can use chrome browser or other browsers to find the xpath of the next button
                nextButtonXPath = '' 
                next = self.driver.find_element_by_xpath(nextButtonXPath)
                next.click()
                print " >>>>> next button clicked"
            except:
                break

        hxs = Selector(text=self.driver.page_source)
        # get the xpath of iterated li which you want to crawl
        iteratedObjectLiXPath = ''
        objects = hxs.xpath(iteratedObjectLiXPath)
        curNo = 1

        for o in objects:
            wholeText = o.xpath('a/span/strong/text()').extract()
            # when the web structure is constructed as a list, you can make those as one string to use join function
            # '@' means class identifier 
            tempCurTitle = ''.join(o.xpath('@data-title').extract())
            # 'urllib.unquote' means that it replaces %xx to its single-charater
            curTitle = urllib.unquote(tempCurTitle)
            print " >>>>> current title:", curTitle
            
            # 'some_class_id' is the class identifier that you want to get the text of 
            #store.xpath('//*[contains(concat(" ", normalize-space(@class), " "), "some_class_id")]')
            
            # stringObject.strip() is working like a trip function
            # listName = [], list initialization
            # listNmae.append(string), list append
            
            curNo = curNo + 1
            
            # item yield
            item = GetFromSearchEngineItem()
            
            # you can use item as you describe in the item python file
            item['title'] = ''.join(curTitle)
            # you can also use the parameter from __init__ method, as it saves in the self object
            item['parameter'] = self.parameter
            
            # when you yield item it will invoke pipelines python file to do the job you make
            yield item
        
        # once it finish its work, you must close the driver 
        self.driver.close()
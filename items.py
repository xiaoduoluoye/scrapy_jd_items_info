# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongGtx1060Item(scrapy.Item):
    # define the fields for your item here like:
    item_name = scrapy.Field()
    item_url = scrapy.Field()
    item_price = scrapy.Field()
    item_shopinfo = scrapy.Field()
    item_haveornot= scrapy.Field()

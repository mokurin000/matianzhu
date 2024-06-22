# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MatianzhuItem(scrapy.Item):
    # define the fields for your item here like:
    source = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

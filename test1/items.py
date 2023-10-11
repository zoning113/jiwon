# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsCrawlingItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    image_url = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    site_location = scrapy.Field()
    site_organizer = scrapy.Field()
    site_type = scrapy.Field()
    sentiment = scrapy.Field()
    confidence = scrapy.Field()
    
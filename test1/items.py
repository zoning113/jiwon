# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsCrawlingItem(scrapy.Item):
    site_name = scrapy.Field()
    site_subject = scrapy.Field()
    site_content = scrapy.Field()
    site_source = scrapy.Field()
    site_image = scrapy.Field()
    contents_type = scrapy.Field()
    content_section = scrapy.Field()
    created_at = scrapy.Field()
    site_location = scrapy.Field()
    
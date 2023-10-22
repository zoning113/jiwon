from __future__ import unicode_literals
from scrapy.exceptions import DropItem
from test1.items import NewsCrawlingItem
from db_import import import_data_to_db

# NLP
from datetime import datetime, timedelta


# 크롤링 된 title 에서 불필요한 words 필터
class WordPipeline(object):
    words_to_filter = [u'PRO', u'[유튜브]', u'[채용 정보]', u'【알립니다】']
    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if any(key in item['site_subject'] for key in self.words_to_filter):
                raise DropItem()
            else:
                return item
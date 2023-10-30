from __future__ import unicode_literals
from scrapy.exceptions import DropItem
from test1.items import NewsCrawlingItem
from db_import import import_data_to_db

# NLP
from datetime import datetime, timedelta


#1. 제목/내용 문장 잇기
class ContentPipeline:
    def process_item(self, item, spider):
        if 'site_content' in item:
            item['site_content'] = ' '.join(item['site_content'])
            item['site_content'] = item['site_content'].replace('\xa0', '').replace('\r\n', '') #2번
        return item

#2. 제목/내용 쓸데없는 \n \t 등 특수문자 제외하기
#item['site_content'] = [text.strip() for text in item['site_content'] if text.strip()]     # 공백 문자열 삭제

#3. 날짜 형식 통일
#class DatePipeline:
    #def process_item(self, item, spider):
        if 'created_at' in item:
            try:
                # Parse the date string into a datetime object
                date_obj = datetime.strptime(item['created_at'], '%d-%m-%Y')
                
                # Format the datetime object into the desired format
                formatted_date = date_obj.strftime('%Y-%m-%d')
                item['created_at'] = formatted_date
            except ValueError:
                pass
        return item

#4. 중복 글 제거

#5. 키워드 중심으로 무관한 주제 글 제외
# 크롤링 된 title 에서 불필요한 words 필터
class WordPipeline(object):
    words_to_filter = [u'PRO', u'[유튜브]', u'[채용 정보]', u'【알립니다】']
    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if any(key in item['site_subject'] for key in self.words_to_filter):
                raise DropItem()
            else:
                return item
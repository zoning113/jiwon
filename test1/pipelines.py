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
            #item['site_content'] = ' '.join(item['site_content'])
            item['site_content'] = [' '.join(text.strip() for text in item['site_content'] if text.strip())] #2번
        return item

#2. 제목/내용 쓸데없는 \n \t 등 특수문자 제외하기(위 코드와 병합)
#item['site_content'] = [text.strip() for text in item['site_content'] if text.strip()]     # 공백 문자열 삭제

#from bs4 import BeautifulSoup                  #구글링
#def remove_html_tags(text):
    #soup = BeautifulSoup(text, "html.parser")
    #return soup.get_text()

#3. 날짜 형식 통일
#date_formats 모든 형태 입력 & "%Y-%m-%d %H:%M" 통일 형태 논의
class DatePipeline:
    def process_item(self, item, spider):
        date_formats = ["%d-%m-%Y", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d %B %Y", "%Y.%m.%d %H:%M"] 
        
        date_str = item['created_at']
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, date_format)
                item['created_at'] = parsed_date.strftime("%Y-%m-%d %H:%M") #시간이 없는 사이트 고려한다면 아래 코드 활용
                #if date_format == "%Y-%m-%d %H:%M":
                    #item['created_at'] = parsed_date.strftime("%Y-%m-%d %H:%M")
                #else:
                    #item['created_at'] = parsed_date.strftime("%Y-%m-%d")
                return item
                return item
            except ValueError:
                continue

        return item



#4. 중복 글 제거
import hashlib
class DuplicateItemFilterPipeline:
    def __init__(self):
        self.processed_items = set()

    def process_item(self, item, spider):
        # Calculate a unique hash for the item, e.g., using its URL
        # 중복 글의 site_source 확인 필요
        item_hash = hashlib.md5(item['site_source'].encode('utf-8')).hexdigest()

        if item_hash in self.processed_items:
            # Skip processing if the item is a duplicate
            raise DropItem(f"Duplicate item found: {item['site_source']}")
        else:
            # Add the item's hash to the set to mark it as processed
            self.processed_items.add(item_hash)
            return item

#5. 키워드 중심으로 무관한 주제 글 제외
# 크롤링 된 title 에서 불필요한 words 필터
class WordPipeline(object):
    words_to_filter = [u'PRO', u'[유튜브]', u'[채용 정보]', u'【알립니다】', u'podcast', u'Webinar', u'Exclusive Video:']
    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if any(key in item['site_subject'] for key in self.words_to_filter):
                raise DropItem()
            else:
                return item
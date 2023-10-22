import scrapy
from pytz import timezone
import datetime as dt
from dateutil.parser import parse
from test1.items import NewsCrawlingItem
class NewsCrawlingSpider(scrapy.Spider):
    name = "mybots"
    now = dt.datetime.now(timezone('Asia/Seoul')).replace(tzinfo=None)

    # 크롤링 페이지를 요청한다 (페이지네이션으로 이루어진 페이지는 2 페이지까지 요청)
    def start_requests(self):
        for i in range(1, 2):
            yield scrapy.Request("https://www.hankyung.com/esg/now?page=%d" % i, self.parse_hankyung)                          # 한경ESG

    # 뉴스 리스트 페이지에서 24시간 이내의 기사만 선별 후 해당 기사 페이지를 요청한다. (뉴스 리스트 페이지에서 'link', 'category' 'date' 데이터 파싱 후 callback)
    def parse_hankyung(self, response):
        for sel in response.xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[1]'):
            #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[1]
            news_date = parse(sel.xpath('.//div[@class="txt-cont"]/span/text()').extract()[0].strip())
            #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[1]/div/span
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = sel.xpath('div[@class="txt-cont"]/h2/a/@href').extract()[0].strip()
                #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[1]/div/h2/a
                item['content_section'] = 'Gen'
                item['created_at'] = sel.xpath('.//div[@class="txt-cont"]/span/text()').extract()[0].strip()
                #image 유무 확인
                it_has_image = response.xpath('.//div[@class="section-news-wrap"]/ul/li/div[@class="thumb"]')
                if it_has_image:
                    item['site_image'] = True
                    item['site_image'] = sel.xpath('.//div[@class="thumb"]/a/img/@src').extract()[0].strip()
                else:
                    item['site_image'] = False
                #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[5]/div[2]
                #item['site_image'] = sel.xpath('a/img/@src').extract()[0].strip()
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                request = scrapy.Request(item['site_source'], callback=self.parse_hankyung2)
                request.meta['item'] = item
                yield request

    # 24시간 이내의 기사들의 본문과 타이틀을 파싱한다.
    def parse_hankyung2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@class="article container v2"]/h1/text()').extract()
        #//*[@id="container"]/div/div/article/h1
        item['site_content'] = response.xpath('//*[@id="article-body]/div/text()').extract()
        #//*[@id="articletxt"]
        #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[2]/div/h2/a
        yield item
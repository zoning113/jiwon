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
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="txt-cont"]/span/text()').extract()[0].strip())
            #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[1]/div/span
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = sel.xpath('div[@class="txt-cont"]/h2/a/@href').extract()[0].strip()
                #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[1]/div/h2/a
                #삭제item['category'] = sel.xpath('div[@class="view-cont"]/span/em[1]/text()').extract()[0].strip()
                #삭제item['date'] = sel.xpath('div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip()
                item['content_section'] = None
                item['created_at'] = sel.xpath().extract()[0].strip()
                #수정필요&xpath
                item['site_image'] = sel.xpath('a/img/@src').extract()[0].strip()
                #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[3]/div[2]/a/img
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                request = scrapy.Request(item['site_source'], callback=self.parse_hankyung)
                request.meta['item'] = item
                yield request

    # 24시간 이내의 기사들의 본문과 타이틀을 파싱한다.
    def parse_hankyung2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@class="txt-cont"]/h2/a/text()').extract()[0].strip()
        #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[2]/div/h2/a
        # item['image_url'] = response.xpath('//*[@id="article-view-content-div"]/div[2]/figure/div/img/@src').extract()[0].strip()
        for sel in response.xpath('//*[@class=""]'):
        #수정필요
        #//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li[2]/div/h2/a
            item['site_content'] = sel.xpath('p/text()').extract()
        yield item
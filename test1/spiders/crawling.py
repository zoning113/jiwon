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
            #yield scrapy.Request("https://www.hankyung.com/esg/now?page=%d" % i, self.parse_hankyungesg)                          # 한경ESG
            #yield scrapy.Request("https://www.greenpostkorea.co.kr/news/articleList.html?page=%d&total=62324&box_idxno=&sc_section_code=S1N62&view_type=sm" % i, self.parse_gpkor_green)    #그린포스트코리아_녹색경제
            #yield scrapy.Request("https://www.greenpostkorea.co.kr/news/articleList.html?page=%d&total=4937&box_idxno=&sc_section_code=S1N61&view_type=sm" % i, self.parse_gpkor_esgmanage) #그린포스트코리아_ESG경영
            #yield scrapy.Request("https://www.greenpostkorea.co.kr/news/articleList.html?page=%d&total=9564&box_idxno=&sc_section_code=S1N65&view_type=sm" % i, self.parse_gpkor_esgfinance) #그린포스트코리아_ESG금융
            yield scrapy.Request("http://www.hansbiz.co.kr/news/articleList.html?page=%d&total=1228&box_idxno=&sc_section_code=S1N37&view_type=sm" % i, self.parse_hansbiz) #한스비즈

    #한경ESG
    # 뉴스 리스트 페이지에서 24시간 이내의 기사만 선별 후 해당 기사 페이지를 요청한다. (뉴스 리스트 페이지에서 'link', 'category' 'date' 데이터 파싱 후 callback)
    def parse_hankyungesg(self, response):
        for sel in response.xpath('//*[@id="container"]/div/div[1]/div[2]/div/div[2]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="txt-cont"]/span/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = sel.xpath('div[@class="txt-cont"]/h2/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="txt-cont"]/span/text()').extract()[0].strip().split(maxsplit=1)[1]
                #site_image 유무 확인 필요함
                item['site_image'] = None
                item['content_section'] = 'Gen'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '한경ESG'
                request = scrapy.Request(item['site_source'], callback=self.parse_hankyungesg2)
                request.meta['item'] = item
                yield request

    # 24시간 이내의 기사들의 본문과 타이틀을 파싱한다.
    def parse_hankyungesg2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="container"]/div/div/article/h1/text()').extract()[0].strip()
        item['site_content'] = response.xpath('//*[@id="articletxt"]/text()').extract()

        yield item

    #그린포스트코리아_녹색경제
    def parse_gpkor_green(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.greenpostkorea.co.kr' + sel.xpath('.//div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1]
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0].strip()
                item['content_section'] = 'E'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '그린포스트코리아'
                request = scrapy.Request(item['site_source'], callback=self.parse_gpkor_green2)
                request.meta['item'] = item
                yield request

    def parse_gpkor_green2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()
        yield item

    #그린포스트코리아_ESG경영
    def parse_gpkor_esgmanage(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.greenpostkorea.co.kr' + sel.xpath('.//div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1]
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0].strip()
                item['content_section'] = 'Gen'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '그린포스트코리아'
                request = scrapy.Request(item['site_source'], callback=self.parse_gpkor_esgmanage2)
                request.meta['item'] = item
                yield request

    def parse_gpkor_esgmanage2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()
        yield item

    #그린포스트코리아_ESG금융
    def parse_gpkor_esgfinance(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.greenpostkorea.co.kr' + sel.xpath('.//div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1]
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0].strip()
                item['content_section'] = 'Gen'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '그린포스트코리아'
                request = scrapy.Request(item['site_source'], callback=self.parse_gpkor_esgfinance2)
                request.meta['item'] = item
                yield request

    def parse_gpkor_esgfinance2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()
        yield item

    #한스경제
    def parse_hansbiz(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=9):
                item = NewsCrawlingItem()
                item['site_source'] = 'http://www.hansbiz.co.kr' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1]
                item['site_image'] = sel.xpath('a/img/@src').extract()[0].strip()
                item['content_section'] = 'Gen'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '한스경제'
                request = scrapy.Request(item['site_source'], callback=self.parse_hansbiz2)
                request.meta['item'] = item
                yield request

    # 24시간 이내의 기사들의 본문과 타이틀을 파싱한다.
    def parse_hansbiz2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()
        yield item
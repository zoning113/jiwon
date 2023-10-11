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
            yield scrapy.Request("https://www.esgtoday.com/category/esg-news/page/%d/" % i, self.parse_esgtoday)  # ESG Today
            yield scrapy.Request("https://www.sporbiz.co.kr/news/articleList.html?page=%d&total=371&box_idxno=&sc_section_code=S1N37&view_type=sm" % i, self.parse_sporbiz)     # 한스경제
            yield scrapy.Request("http://www.econovill.com/news/articleList.html?page=%d&total=762&box_idxno=&sc_serial_code=SRN559&view_type=sm" % i, self.parse_econovill)    # 이코노믹리뷰
            yield scrapy.Request("http://www.esgeconomy.com/news/articleList.html?page=%d&total=1384&box_idxno=&view_type=sm" % i, self.parse_esgeconomy)                       # ESG 경제
            yield scrapy.Request("https://www.impacton.net/news/articleList.html?page=%d&total=2705&box_idxno=&view_type=sm" % i, self.parse_impacton)                          # 임팩트온

    # 뉴스 리스트 페이지에서 24시간 이내의 기사만 선별 후 해당 기사 페이지를 요청한다. (뉴스 리스트 페이지에서 'link', 'category' 'date' 데이터 파싱 후 callback)
    def parse_sporbiz(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['link'] = 'https://www.sporbiz.co.kr' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['category'] = sel.xpath('div[@class="view-cont"]/span/em[1]/text()').extract()[0].strip()
                item['date'] = sel.xpath('div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip()
                item['image_url'] = sel.xpath('a/img/@src').extract()[0].strip()
                item['site_location'] = 'kor'
                item['site_type'] = 'news'
                item['site_organizer'] = 'news'
                request = scrapy.Request(item['link'], callback=self.parse_sporbiz2)
                request.meta['item'] = item
                yield request

    # 24시간 이내의 기사들의 본문과 타이틀을 파싱한다.
    def parse_sporbiz2(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        # item['image_url'] = response.xpath('//*[@id="article-view-content-div"]/div[2]/figure/div/img/@src').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['content'] = sel.xpath('p/text()').extract()

        
        yield item



    def parse_econovill(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['link'] = 'http://www.econovill.com' + sel.xpath('h4/a/@href').extract()[0].strip()
                item['date'] = sel.xpath('span/em[3]/text()').extract()[0].strip()
                item['category'] = sel.xpath('span/em[1]/text()').extract()[0].strip()
                item['image_url'] = sel.xpath('a/img/@src').extract()[0].strip()
                item['site_location'] = 'kor'
                item['site_type'] = 'news'
                item['site_organizer'] = 'news'
                request = scrapy.Request(item['link'], callback=self.parse_econovill2)
                request.meta['item'] = item
                yield request

    def parse_econovill2(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        # item['image_url'] = response.xpath('//*[@id="article-view-content-div"]/div[1]/figure/div/img/@src').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['content'] = sel.xpath('p/text()').extract()
        yield item




    def parse_esgeconomy(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('div/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['link'] = 'http://www.esgeconomy.com' + sel.xpath('div/h4/a/@href').extract()[0].strip()
                item['date'] = sel.xpath('div/span/em[3]/text()').extract()[0].strip()
                item['category'] = sel.xpath('div/span/em[1]/text()').extract()[0].strip()
                item['image_url'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0].strip()
                item['site_location'] = 'kor'
                item['site_type'] = 'news'
                item['site_organizer'] = 'news'
                request = scrapy.Request(item['link'], callback=self.parse_esgeconomy2)
                request.meta['item'] = item
                yield request

    def parse_esgeconomy2(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['content'] = sel.xpath('p/text()').extract()
        yield item




    def parse_impacton(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                if sel.xpath('h4/a/span/text()').get() is None:
                    item = NewsCrawlingItem()
                    item['link'] = 'https://www.impacton.net/' + sel.xpath('h4/a/@href').extract()[0].strip()
                    item['date'] = sel.xpath('span/em[3]/text()').extract()[0].strip()
                    item['category'] = sel.xpath('span/em[1]/text()').extract()[0].strip()
                    item['image_url'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0].strip()
                    item['site_location'] = 'kor'
                    item['site_type'] = 'news'
                    item['site_organizer'] = 'news'
                    request = scrapy.Request(item['link'], callback=self.parse_impacton2)
                    request.meta['item'] = item
                    yield request

    def parse_impacton2(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['content'] = sel.xpath('p/text()').extract()
        yield item




    def parse_esgtoday(self, response):
        sel = response.xpath("//*[@id='loops-wrapper']")
        for sel1 in sel.css("article"):
            news_date = parse(sel1.xpath("div/p/time/text()").extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=2):
                item = NewsCrawlingItem()
                item['title'] = sel1.xpath("div/h2/a/text()").extract()[0].strip()
                item['link'] = sel1.xpath("div/h2/a/@href").extract()[0].strip()
                item['date'] = news_date
                item['category'] = sel1.xpath("div/p[1]/span/a[1]/text()").extract()[0].strip()
                item['image_url'] = 'https://source.unsplash.com/500x500/?business'
                item['site_location'] = 'glo'
                item['site_type'] = 'news'
                item['site_organizer'] = 'news'
                request = scrapy.Request(item['link'], callback=self.parse_esgtoday2)
                request.meta['item'] = item
                yield request

    def parse_esgtoday2(self, response):
        item = response.meta['item']
        sel = response.xpath("//*[@id='content']").css('article')
        for sel in sel.xpath('div/div[3]'):
            item['content'] = sel.xpath('p/text()').extract()
        yield item
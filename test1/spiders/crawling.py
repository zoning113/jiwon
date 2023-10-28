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
            #yield scrapy.Request("http://www.hansbiz.co.kr/news/articleList.html?page=%d&total=1228&box_idxno=&sc_section_code=S1N37&view_type=sm" % i, self.parse_hansbiz) #한스비즈
            #yield scrapy.Request("http://www.greened.kr/news/articleList.html?page=%d&total=2151&box_idxno=&sc_section_code=S1N18&view_type=sm" % i, self.parse_greened_plan) #녹색경제신문_ESG기획
            #yield scrapy.Request("http://www.greened.kr/news/articleList.html?page=%d&total=556&box_idxno=&sc_section_code=S1N28&view_type=sm" % i, self.parse_greened_trend) #녹색경제신문_ESG동향
            #yield scrapy.Request("http://www.greened.kr/news/articleList.html?page=%d&total=3738&box_idxno=&sc_section_code=S1N29&view_type=sm" % i, self.parse_greened_economy) #녹색경제신문_함께하는경제
            #yield scrapy.Request("https://www.impacton.net/news/articleList.html?page=%d&total=1836&box_idxno=&sc_section_code=S1N1&view_type=sm" % i, self.parse_impacton_indus) #임팩트온_산업
            #yield scrapy.Request("https://www.impacton.net/news/articleList.html?page=%d&total=945&box_idxno=&sc_section_code=S1N2&view_type=sm" % i, self.parse_impacton_policy) #임팩트온_정책
            #yield scrapy.Request("https://www.impacton.net/news/articleList.html?page=%d&total=657&box_idxno=&sc_section_code=S1N9&view_type=sm" % i, self.parse_impacton_inv) #임팩트온_투자&평가
            #yield scrapy.Request("https://www.impacton.net/news/articleList.html?page=%d&total=492&box_idxno=&sc_sub_section_code=S2N14&view_type=sm" % i, self.parse_impacton_issue) #임팩트온_이슈핫클립
            #yield scrapy.Request("https://www.esgeconomy.com/news/articleList.html?page=%d&total=1054&box_idxno=&sc_section_code=S1N1&view_type=sm" % i, self.parse_esgeconomy_sus) #ESG경제_지속가능경제
            yield scrapy.Request("https://www.esgeconomy.com/news/articleList.html?page=%d&total=537&box_idxno=&sc_sub_section_code=S2N3&view_type=sm" % i, self.parse_esgeconomy_env) #ESG경제_환경
            yield scrapy.Request("https://www.esgeconomy.com/news/articleList.html?page=%d&total=69&box_idxno=&sc_sub_section_code=S2N4&view_type=sm" % i, self.parse_esgeconomy_soc) #ESG경제_사회
            #yield scrapy.Request("https://www.esgeconomy.com/news/articleList.html?page=%d&total=861&box_idxno=&sc_section_code=S1N8&view_type=sm" % i, self.parse_esgeconomy_gov) #ESG경제_기업거버넌스
            #yield scrapy.Request("https://www.esgeconomy.com/news/articleList.html?page=%d&total=672&box_idxno=&sc_section_code=S1N5&view_type=sm" % i, self.parse_esgeconomy_ass) #ESG경제_공시평가
            #yield scrapy.Request("https://www.esgeconomy.com/news/articleList.html?page=%d&total=107&box_idxno=&sc_section_code=S1N7&view_type=sm" % i, self.parse_esgeconomy_opi) #ESG경제_오피니언


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
            if self.now - news_date < dt.timedelta(days=1):
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

    #녹색경제신문_ESG기획
    #image 확인
    def parse_greened_plan(self, response):
        for sel in response.xpath('//*[@id="user-container"]/div[4]/div[2]/section/article/div[2]/section/div'):
            news_date = parse(sel.xpath('.//div[@class="list-dated"]/text()').extract()[0].split('|')[2].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'http://www.greened.kr' + sel.xpath('div[@class="list-titles"]/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="list-dated"]/text()').extract()[0].split('|')[2].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('.//div[@class="list-image"]/@style').extract()[0]
                item['content_section'] = None
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '녹색경제신문'
                request = scrapy.Request(item['site_source'], callback=self.parse_greened_plan2)
                request.meta['item'] = item
                yield request

    def parse_greened_plan2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('///*[@id="user-container"]/div[4]/header/div/div/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="articleBody"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #녹색경제신문_ESG동향
    def parse_greened_trend(self, response):
        for sel in response.xpath('//*[@id="user-container"]/div[4]/div[2]/section/article/div[2]/section/div'):
            news_date = parse(sel.xpath('.//div[@class="list-dated"]/text()').extract()[0].split('|')[2].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'http://www.greened.kr' + sel.xpath('div[@class="list-titles"]/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="list-dated"]/text()').extract()[0].split('|')[2].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('.//div[@class="list-image"]/@style').extract()[0]
                item['content_section'] = None
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '녹색경제신문'
                request = scrapy.Request(item['site_source'], callback=self.parse_greened_trend2)
                request.meta['item'] = item
                yield request

    def parse_greened_trend2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('///*[@id="user-container"]/div[4]/header/div/div/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="articleBody"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #녹색경제신문_함께하는경제
    def parse_greened_economy(self, response):
        for sel in response.xpath('//*[@id="user-container"]/div[4]/div[2]/section/article/div[2]/section/div'):
            news_date = parse(sel.xpath('.//div[@class="list-dated"]/text()').extract()[0].split('|')[2].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'http://www.greened.kr' + sel.xpath('div[@class="list-titles"]/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="list-dated"]/text()').extract()[0].split('|')[2].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('.//div[@class="list-image"]/@style').extract()[0]
                item['content_section'] = None
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '녹색경제신문'
                request = scrapy.Request(item['site_source'], callback=self.parse_greened_economy2)
                request.meta['item'] = item
                yield request

    def parse_greened_economy2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('///*[@id="user-container"]/div[4]/header/div/div/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="articleBody"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #임팩트온_산업
    def parse_impacton_indus(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.impacton.net' + sel.xpath('.//div[@class="view-cont"]/h2/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = None
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '임팩트온'
                request = scrapy.Request(item['site_source'], callback=self.parse_impacton_indus2)
                request.meta['item'] = item
                yield request
    
    def parse_impacton_indus2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h1/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #임팩트온_정책
    def parse_impacton_policy(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.impacton.net' + sel.xpath('.//div[@class="view-cont"]/h2/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = None
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '임팩트온'
                request = scrapy.Request(item['site_source'], callback=self.parse_impacton_policy2)
                request.meta['item'] = item
                yield request
    
    def parse_impacton_policy2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h1/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #임팩트온_투자&평가
    def parse_impacton_inv(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.impacton.net' + sel.xpath('.//div[@class="view-cont"]/h2/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = None
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = '임팩트온'
                request = scrapy.Request(item['site_source'], callback=self.parse_impacton_inv2)
                request.meta['item'] = item
                yield request
    
    def parse_impacton_inv2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h1/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item


    #임팩트온_이슈핫클립
    def parse_impacton_issue(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.impacton.net' + sel.xpath('.//div[@class="view-cont"]/h2/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = 'Gen'
                item['site_location'] = 'KR'
                item['contents_type'] = 'issueclip'
                item['site_name'] = '임팩트온'
                request = scrapy.Request(item['site_source'], callback=self.parse_impacton_issue2)
                request.meta['item'] = item
                yield request
    
    def parse_impacton_issue2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h1/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #ESG경제_지속가능경제
    def parse_esgeconomy_env(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.esgeconomy.com' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = 'E'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = 'ESG경제'
                request = scrapy.Request(item['site_source'], callback=self.parse_esgeconomy_env2)
                request.meta['item'] = item
                yield request

    def parse_esgeconomy_env2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #ESG경제_지속가능경제
    def parse_esgeconomy_sus(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.esgeconomy.com' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = 'E'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = 'ESG경제'
                request = scrapy.Request(item['site_source'], callback=self.parse_esgeconomy_sus2)
                request.meta['item'] = item
                yield request

    def parse_esgeconomy_sus2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #ESG경제_환경
    def parse_esgeconomy_env(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=3):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.esgeconomy.com' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = 'E'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = 'ESG경제'
                request = scrapy.Request(item['site_source'], callback=self.parse_esgeconomy_env2)
                request.meta['item'] = item
                yield request

    def parse_esgeconomy_env2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #ESG경제_사회
    def parse_esgeconomy_soc(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=16):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.esgeconomy.com' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = 'S'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = 'ESG경제'
                request = scrapy.Request(item['site_source'], callback=self.parse_esgeconomy_soc2)
                request.meta['item'] = item
                yield request

    def parse_esgeconomy_soc2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #ESG경제_기업거버넌스
    def parse_esgeconomy_gov(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.esgeconomy.com' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = 'G'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = 'ESG경제'
                request = scrapy.Request(item['site_source'], callback=self.parse_esgeconomy_gov2)
                request.meta['item'] = item
                yield request

    def parse_esgeconomy_gov2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #ESG경제_공시평가
    def parse_esgeconomy_ass(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.esgeconomy.com' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = 'Gen'
                item['site_location'] = 'KR'
                item['contents_type'] = 'news'
                item['site_name'] = 'ESG경제'
                request = scrapy.Request(item['site_source'], callback=self.parse_esgeconomy_ass2)
                request.meta['item'] = item
                yield request

    def parse_esgeconomy_ass2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item

    #ESG경제_오피니언
    def parse_esgeconomy_opi(self, response):
        for sel in response.xpath('//*[@id="section-list"]/ul/li'):
            news_date = parse(sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].strip())
            if self.now - news_date < dt.timedelta(days=1):
                item = NewsCrawlingItem()
                item['site_source'] = 'https://www.esgeconomy.com' + sel.xpath('div[@class="view-cont"]/h4/a/@href').extract()[0].strip()
                item['created_at'] = sel.xpath('.//div[@class="view-cont"]/span/em[3]/text()').extract()[0].split(maxsplit=1)[1].strip()
                item['site_image'] = sel.xpath('a[@class="thumb"]/img/@src').extract()[0]
                item['content_section'] = None
                item['site_location'] = 'KR'
                item['contents_type'] = None #알림/칼럼 분류 필요함
                item['site_name'] = 'ESG경제'
                request = scrapy.Request(item['site_source'], callback=self.parse_esgeconomy_opi2)
                request.meta['item'] = item
                yield request

    def parse_esgeconomy_opi2(self, response):
        item = response.meta['item']
        item['site_subject'] = response.xpath('//*[@id="article-view"]/div/header/h3/text()').extract()[0].strip()
        for sel in response.xpath('//*[@id="article-view-content-div"]'):
            item['site_content'] = sel.xpath('p/text()').extract()

        yield item
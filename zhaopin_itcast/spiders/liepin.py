# # -*- coding: utf-8 -*-
# from datetime import datetime
# from urllib.parse import urljoin
#
# import scrapy
# from scrapy_redis.spiders import RedisSpider
#
# from zhaopin_itcast.settings import CITY, KEYWORDS, DAYS
#
#
# class LiepinSpider(RedisSpider):
#     name = 'liepin'
#     allowed_domains = ['liepin.com']
#     redis_key = 'liepin'
#     custom_settings = {
#         'DEFAULT_REQUEST_HEADERS': {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
#         },
#         'COOKIES_ENABLED': False,
#         'LOG_LEVEL ': 'DEBUG',
#         # 'REDIS_PARAMS': {'password': 'Lxcc198#!', 'db': 3}
#     }
#     city_data = {
#         u"北京": "010",
#         u"上海": "020",
#         u"广州": "050020",
#         u"深圳": "050090",
#         u"武汉": "170020",
#         u"成都": "280020",
#         u"重庆": "040",
#         u"郑州": "150020",
#         u"杭州": "070020",
#         u"济南": "250020",
#         u"南京": "060020",
#         u"西安": "270020",
#         u"长沙": "180020",
#         u"哈尔滨": "160020",
#         u"石家庄": "140020",
#         u"合肥": "080020",
#         u"太原": "260020",
#         u"厦门": "090040",
#         u"苏州": "060080",
#         u"天津": "030",
#         u"沈阳": "210020",
#         u"青岛": "250070",
#         u"无锡": "060100",
#         u"昆明": "310020",
#         u"大连": "210040",
#         u"福州": "090020",
#         u"长春": "190020",
#         u"南昌": "200020",
#     }
#     search_api = 'https://www.liepin.com/zhaopin/?pubTime={days}&dqs={loc}&key={kw}&curPage={page}'
#
#     def start_requests(self):
#         self.days = DAYS
#         for city in CITY:
#             for keyword, filter_kw in KEYWORDS:
#                 city_num = self.city_data[city]
#                 url = self.search_api.format(loc=city_num, days=self.days, kw=keyword, page=0)
#                 yield scrapy.Request(url, self.list_parse, meta={
#                     'dt': {"city": city, 'city_num': city_num, "keyword": keyword, "filter": filter_kw}})
#
#     def list_parse(self, response):
#         dt = response.meta['dt']
#         filter_kw = dt['filter']
#         detail_links = response.xpath('//ul[@class="sojob-list"]//h3/a/@href').extract()
#         detail_names = response.xpath('//ul[@class="sojob-list"]//h3/a/text()').extract()
#         detail_names = [i.strip() for i in detail_names]
#         detail_dt = dict(zip(detail_links, detail_names))
#         for link, job_name in detail_dt.items():
#             for fkw in filter_kw:
#                 if fkw.lower() in job_name.lower():
#                     link = urljoin('https://www.liepin.com/', link)
#                     yield scrapy.Request(link, self.detail_parse, meta={'dt': dt})
#
#         next_url = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
#         if 'javascript' not in next_url:
#             next_url = urljoin('https://www.liepin.com/', next_url)
#             print('翻页', next_url)
#             yield scrapy.Request(next_url, self.list_parse, meta={'dt': dt})
#
#     def detail_parse(self, response):
#         url = response.url
#         if '?imscid' not in url:
#             dt = response.meta['dt'].copy()
#             filter_kw = ','.join(dt['filter'])
#             sub_name = response.xpath('//div[contains(@class,"title-info")]/h1/text()') or \
#                        response.xpath('//div[contains(@class,"job-title")]/h1/text()')
#             sub_name = sub_name.extract_first()
#             company_name = response.xpath('//div[@class="title-info"]//h3/a/text()')or \
#                            response.xpath('//div[contains(@class,"job-title")]/h2/text()') or \
#                            response.xpath('//div[contains(@class,"title-info")]//h3/text()')
#             company_name = company_name.extract_first().strip()
#             salary = response.xpath('//div[@class="job-title-left"]/p[@class="job-item-title"]/text()') or \
#                      response.xpath('//div[@class="job-title-left"]/p[@class="job-main-title"]/text()')
#             salary = salary.extract_first() or  ''
#             salary = salary.strip()
#             salary = self.salary_format(salary)
#             pub_date = response.xpath('//div[@class="job-title-left"]//p[@class="basic-infor"]/time/@title')\
#                 .extract_first() or response.xpath('//span[contains(text(),"发布于：")]/text()').extract_first().replace('发布于：', '')
#             pub_date = pub_date.replace('年', '-').replace('月', '-').replace('日', '')
#             info = response.xpath('//div[@class="job-qualifications"]//span/text()').extract() or\
#                    response.xpath('//div[@class="resume clearfix"]//span/text()').extract() or \
#                    response.xpath('//p[@class="job-qualifications"]//span/text()').extract()
#             education_background, experience, *oth = info
#             company_area = response.xpath('//li[contains(text(),"行业：")]/a/text()').extract_first() or \
#                            response.xpath('//li[contains(text(),"领域/融资：")]/text()').extract_first() or ''
#             company_area = company_area.replace('领域/融资：', '')
#             company_size = response.xpath('//li[contains(text(),"公司规模：")]/text()').extract_first() or ''
#             company_size = company_size.replace('公司规模：', '')
#             office_address = response.xpath('//li[contains(text(),"公司地址：")]/text()').extract_first() or ''
#             office_address = office_address.replace('公司地址：', '')
#             description = response.xpath('//div[@class="content content-word"]/text()').extract() or\
#                           response.xpath('//div[@class="job-info-content"]/text()').extract()
#             description = ''.join(description).replace('\r\n', '').replace('\t', '').replace('\xa0', '').replace('\n', '')\
#                 .replace(' ', '')
#             now = datetime.now()
#             updatetime = str(now).split(' ')[0]
#             dt.pop('city_num')
#             dt.update({
#                 'url':url,
#                 'job_name': sub_name,
#                 'filter': filter_kw,
#                 'company_name': company_name,
#                 'salary': salary,
#                 'pub_date': pub_date,
#                 'education_background': education_background,
#                 'experience': experience,
#                 'company_area': company_area,
#                 'company_size': company_size,
#                 'office_address': office_address,
#                 'description': description,
#                 'number': '',
#                 'category': '',
#                 'source': 'lp',
#                 'updatetime': updatetime,
#
#             })
#
#             yield dt
#
#     def salary_format(self, sy):
#         salary = sy
#         if salary is not None:
#             if '万' in sy:
#                 salary = salary.replace('万','').split('-')
#                 salary = '-'.join([str(int((float(i)/12)*10000)) for i in salary])
#         return salary
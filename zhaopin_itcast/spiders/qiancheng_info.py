# # -*- coding: utf-8 -*-
# import json
# from datetime import datetime, timedelta
#
# import scrapy
# from scrapy_redis.spiders import RedisSpider
# from zhaopin_itcast.settings import CITY, KEYWORDS, DAYS
# import re
#
# class QianchengSpider(RedisSpider):
#     name = 'qiancheng'
#     allowed_domains = ['51job.com']
#     redis_key = 'qiancheng'
#     lt = []
#     custom_settings = {
#         'DEFAULT_REQUEST_HEADERS': {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
#         },
#         'COOKIES_ENABLED': False,
#         'LOG_LEVEL ': 'DEBUG',
#     }
#     city_data = {
#         u"北京": "010000",
#         u"上海": "020000",
#         u"广州": "030200",
#         u"深圳": "040000",
#         u"武汉": "180200",
#         u"成都": "090200",
#         u"重庆": "060000",
#         u"郑州": "170200",
#         u"杭州": "080200",
#         u"济南": "120200",
#         u"南京": "070200",
#         u"西安": "200200",
#         u"长沙": "190200",
#         u"哈尔滨": "220200",
#         u"石家庄": "160200",
#         u"合肥": "150200",
#         u"太原": "210200",
#         u"厦门": "110300",
#         u"沈阳": "230200",
#         u"大连": "230300",
#         u"苏州": "070300",
#         u"天津": "050000",
#         u"青岛": "120300",
#         u"无锡": "070400",
#         u"昆明": "250200",
#         u"福州": "110200",
#         u"长春": "240200",
#         u"南昌": "130200",
#     }
#     params = '?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
#     search_api = 'https://search.51job.com/list/{loc},000000,0000,00,{days},99,{kw},2,{page}.html%s' % params
#     def start_requests(self):
#         self.days = DAYS
#         if self.days == 7:
#             self.days = 2
#         for city in CITY:
#             for keyword, filter_kw in KEYWORDS:
#                 city_num = self.city_data[city]
#                 url = self.search_api.format(loc=city_num,days=self.days,kw=keyword,page=1)
#                 yield scrapy.Request(url,self.list_parse,meta={'dt':{"city": city, 'city_num':city_num,"keyword": keyword, "filter":filter_kw}})
#
#     def list_parse(self,response):
#         dt = response.meta['dt']
#         filter_kw = dt['filter']
#         detail_links = response.xpath('//div[@class="el"]/p[contains(@class,"t1")]/span/a/@href').extract()
#         detail_names = response.xpath('//div[@class="el"]/p[contains(@class,"t1")]/span/a/text()').extract()
#         detail_names = [i.strip() for i in detail_names]
#         detail_dt = dict(zip(detail_links,detail_names))
#         for link,job_name in detail_dt.items():
#             for fkw in filter_kw:
#                 if fkw.lower() in job_name.lower():
#                     yield scrapy.Request(link,self.detail_parse,meta={'dt':dt})
#
#         next_url = response.xpath('//div[@class="p_in"]//li[@class="on"]/following-sibling::li[1]/a/@href').extract_first()
#         if next_url:
#             yield scrapy.Request(next_url, self.list_parse, meta={'dt': dt})
#
#
#     def detail_parse(self,response):
#         dt = response.meta['dt'].copy()
#         filter_kw = dt['filter']
#         url = response.url
#         if 'jobs.51job.com' in url:
#             job_name = response.xpath('//h1/text()').extract_first().strip()
#             company_name = response.xpath('//p[@class="cname"]/a/text()').extract_first().strip()
#             category = response.xpath(
#                 '//div[@class="mt10"]//span[contains(text(),"职能类别：")]/following-sibling::span/text()').extract()
#             category = ','.join(category).replace('-', '').replace('/', '')
#             info = response.xpath('//p[@class="msg ltype"]/text()').extract()[0].split('  |  ')
#             experience = info[1] if '经验' in info[1] else ''
#             education_background = info[2] if '招' not in info[2] else ''  # 学历要求
#             number = [i.replace('招', '') for i in info if '招' in i][0]
#             pub_date = '2018-'+[i for i in info if '发布' in i][0].strip().replace('发布','')
#             description = response.xpath("//div[@class='bmsg job_msg inbox']//text()").extract()
#             description = ''.join(description).replace('\r\n','').replace('\t','').replace('\xa0','')
#             salary = response.xpath("//div[@class='tHeader tHjob']//div[@class='cn']/strong/text()").extract_first()
#             filter_kw = ','.join(filter_kw)
#             office_address = response.xpath('//span[contains(text(),"上班地址：")]/parent::p/text()').extract() or ['']
#             office_address = office_address[1].strip()
#             company_size = response.xpath('//span[@class="i_people"]/parent::p/text()').extract_first()
#             company_area = response.xpath('//span[@class="i_trade"]/parent::p/text()').extract_first()
#             company_info = response.xpath('//div[@class="tCompany_main"]//span[contains(text(),"公司信息")]/parent::h2/following-sibling::div//text()').extract()
#             company_info = ''.join(company_info).replace('\r\n','').replace('\t','').replace('\xa0','')
#             now = datetime.now()
#             updatetime = str(now).split(' ')[0]
#             dt.pop('city_num')
#             dt.update({
#                 'job_name':job_name,
#                 'url':url,
#                 'source':'qc',
#                 'company_name':company_name,
#                 'category':category,
#                 'experience':experience,
#                 'education_background':education_background,
#                 'number':number,
#                 'pub_date':pub_date,
#                 'salary':salary,
#                 'description':description,
#                 'filter':filter_kw,
#                 'office_address':office_address,
#                 'company_size':company_size,
#                 'company_area':company_area,
#                 'company_info':company_info,
#                 'updatetime':updatetime
#
#             })
#             yield dt
#

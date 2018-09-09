# from datetime import datetime
# from urllib.parse import urljoin
#
# import scrapy
# from scrapy_redis.spiders import RedisSpider
# from zhaopin_itcast.settings import CITY, KEYWORDS, DAYS
# import json
# from urllib.parse import quote
# from datetime import datetime,timedelta
# import hashlib
#
# def yesterday(days=DAYS):
#     now = datetime.now()
#     yesterday = now - timedelta(days=days)
#     y = str(yesterday.date())
#     y = y.replace('-', '')
#     return int(y), str(now).split(' ')[0]
#
# def md(st):
#     md = hashlib.md5()
#     md.update(st.encode('utf-8'))
#     return md.hexdigest()
#
#
# class LogouSpider(RedisSpider):
#     name = 'lagou'
#     allowed_domains = ['www.lagou.com']
#     redis_key = 'lagou'
#     yesterday, updatetime = yesterday()
#     custom_settings = {
#         'DEFAULT_REQUEST_HEADERS': {
#             'Accept': 'application/json, text/javascript, */*; q=0.01',
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'Connection': 'keep-alive',
#             'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#             'Cookie': 'user_trace_token=20170917131719-7a9e9c71-9b67-11e7-959c-525400f775ce; LGUID=20170917131719-7a9e9ec8-9b67-11e7-959c-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; X_HTTP_TOKEN=c0f3e4f54147011461641eac94d65d1a; JSESSIONID=ABAAABAAAFCAAEG53A443AD79DB3B2420CAA10670C23589; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _gat=1; TG-TRACK-CODE=index_navigation; SEARCH_ID=594c1972e6f54172bcb77d92a9165404; _gid=GA1.2.1300189671.1505625437; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505625437; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505726708; _ga=GA1.2.471048555.1505625437; LGSID=20170918170433-6392c82d-9c50-11e7-9693-525400f775ce; LGRID=20170918172509-43d13bee-9c53-11e7-969a-525400f775ce',
#             'Host': 'www.lagou.com',
#             'Origin': 'https://www.lagou.com',
#             'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
#         },
#         'COOKIES_ENABLED': False,
#         'LOG_LEVEL ': 'DEBUG',
#         'DOWNLOAD_DELAY': 1.2,
#         #关闭scrapy的referer中间件,使用headers设定的referer
#         'SPIDER_MIDDLEWARES': {
#         'zhaopin_itcast.middlewares.ZhaopinItcastSpiderMiddleware': 543,
#         'scrapy.spidermiddlewares.referer.RefererMiddleware':None
#         },
#         'REDIS_PARAMS': {'password': 'Lxcc198#!', 'db': 2}
#     }
#     city_data = {
#         u"北京": u"北京",
#         u"上海": u"上海",
#         u"广州": u"广州",
#         u"深圳": u"深圳",
#         u"武汉": u"武汉",
#         u"成都": u"成都",
#         u"重庆": u"重庆",
#         u"郑州": u"郑州",
#         u"杭州": u"杭州",
#         u"济南": u"济南",
#         u"南京": u"南京",
#         u"西安": u"西安",
#         u"长沙": u"长沙",
#         u"哈尔滨": u"哈尔滨",
#         u"石家庄": u"石家庄",
#         u"合肥": u"合肥",
#         u"太原": u"太原",
#         u"厦门": u"厦门",
#         u"苏州": u"苏州",
#         u"天津": u"天津",
#         u"沈阳": u"沈阳",
#         u"青岛": u"青岛",
#         u"无锡": u"无锡",
#         u"昆明": u"昆明",
#         u"大连": u"大连",
#         u"福州": u"福州",
#         u"长春": u"长春",
#         u"南昌": u"南昌",
#     }
#     search_api = 'https://www.lagou.com/jobs/positionAjax.json?px=new&city={loc}&needAddtionalResult=false#'
#
#     def start_requests(self):
#         for city in CITY:
#             form = {
#                 'first': 'true',
#                 'pn': '1',
#                 'kd': 'python'
#             }
#             loc = self.city_data[city]
#             for keyword, filter_kw in KEYWORDS:
#                 form.update({
#                     'kd':keyword
#                 })
#                 st = md(loc+keyword+form['pn'])
#                 url = self.search_api.format(loc=quote(loc))+st
#                 yield scrapy.FormRequest(url=url,callback=self.json_parse,
#                                          formdata=form,meta={'dt':{'city':loc,'keyword':keyword,'filter':filter_kw,'form':form}}
#                                          )
#
#     def json_parse(self,response):
#         dt = response.meta['dt']
#         loc = dt['city']
#         keyword = dt['keyword']
#         form = dt['form']
#         data = json.loads(response.text)
#         resultSize = None
#         if data['success']:
#             positionResult = data['content']['positionResult']
#             results = positionResult['result']
#             for result in results:
#                 createTime = result['createTime'].split(' ')[0]
#                 createTime = int(createTime.replace('-',''))
#
#                 if createTime >= self.yesterday:
#                     job_name = result['positionName']
#                     filter_kw = dt['filter']
#                     for fkw in filter_kw:
#                         if fkw.lower() in job_name.lower():
#                             positionId = result['positionId']
#                             url = 'https://www.lagou.com/jobs/%s.html'% positionId
#                             dt.update({
#                                 'positionId': positionId,
#                                 'job_name': job_name,
#                                 'company_name': result['companyFullName'],
#                                 'pub_date': result['createTime'].split(' ')[0],
#                                 'salary': self.salary_format(result['salary']),
#                                 'education_background': result['education'],
#                                 'experience': result['workYear'],
#                                 'company_size': result['companySize'],
#                                 'company_area': result['industryField'],
#                                 'category': result['firstType'].replace('|',',') + ',' + result['secondType']
#                             })
#                             referer = 'https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput'\
#                                 .format(keyword,quote(loc))
#                             detail_headers = self.custom_settings['DEFAULT_REQUEST_HEADERS'].copy()
#                             detail_headers.update({'Referer':referer})
#                             yield scrapy.Request(url,self.detail_parse,headers=detail_headers,meta={'dt':dt})
#                             break
#             resultSize = int(positionResult['resultSize'])
#             print(resultSize)
#         else:
#             print(data['msg'],data['clientIp'])
#         if resultSize:
#             form['pn'] = str(int(form['pn'])+1)
#             form['first'] = 'false'
#             print('翻页',loc,keyword,form['pn'])
#             st = md(loc+keyword+form['pn'])
#             url = self.search_api.format(loc=quote(loc))+st
#             yield scrapy.FormRequest(url=url,callback=self.json_parse,formdata=form,meta={'dt':dt})
#
#     def detail_parse(self,response):
#         dt = response.meta['dt'].copy()
#         filter_kw = ','.join(dt['filter'])
#         url = response.url
#         description = response.xpath('//dl[@id="job_detail"]/dd[@class="job_bt"]//text()').extract()
#         description = ''.join(description).strip().replace('\n','').replace('\xa0','')\
#             .replace('\u3000','').replace('\uf0fc','').replace(' ','').replace('\r','')
#         office_address = response.xpath('//div[@class="work_addr"]//text()').extract()
#         office_address = ''.join(office_address).replace(' ','').replace('-',',').replace('\n','').replace('查看地图','')
#         dt.pop('form')
#         dt.pop('positionId')
#         dt.update({
#             'url':url,
#             'description':description,
#             'office_address':office_address,
#             'filter':filter_kw,
#             'updatetime':self.updatetime,
#             'number':'',
#             'keywords':'',
#             'source':'lg'
#         })
#
#         yield dt
#
#     def salary_format(self, sy):
#         salary = sy
#         if salary is not None:
#             if 'k' in sy.lower() and '以上' not in sy:
#                 salary = salary.replace('k','').replace('K','').split('-')
#                 salary = '-'.join([str(int(float(i)*1000)) for i in salary])
#             elif '以上' in sy:
#                 salary = salary.replace('k', '').replace('K', '').replace('以上', '')
#                 salary = salary + '-' + salary
#         return salary
#

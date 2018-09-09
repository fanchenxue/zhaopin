# # -*- coding: utf-8 -*-
# import json
# from datetime import datetime, timedelta
#
# import scrapy
# from scrapy_redis.spiders import RedisSpider
#
# from zhaopin_itcast.settings import CITY, KEYWORDS, DAYS
#
#
# class ZhilianSpider(RedisSpider):
#     name = 'zhilian'
#     allowed_domains = ['zhaopin.com']
#     redis_key = 'zhilian'
#
#     custom_settings = {
#         'DEFAULT_REQUEST_HEADERS': {
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'Connection': 'keep-alive',
#             # 旧版cookie
#             'Cookie': '_ga=GA1.2.729308262.1515999800; user_trace_token=20180115150320-2baeff3c-f9c2-11e7-9ad0-525400f775ce; LGUID=20180115150320-2baf01d0-f9c2-11e7-9ad0-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAFCAAEG1E9059DD35CB0074A3CAC41F6F12746D; _gid=GA1.2.31556095.1516618533; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515999802,1516618534; LGSID=20180122185528-c227d701-ff62-11e7-a5a8-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f7Ghk60yUKm0FNkUs0gsvNp00000PW4pNb00000XRRNRW.THL0oUhY1x60UWdBmy-bIfK15yuhnW6dmWcYnj0sPHI-nWn0IHYLnRFDrjnsPWnsfWnzfH7DrHcsrDmzwj9arDR1rjczn0K95gTqFhdWpyfqn101n1csPHnsPausThqbpyfqnHm0uHdCIZwsT1CEQLILIz4_myIEIi4WUvYE5LNYUNq1ULNzmvRqUNqWu-qWTZwxmh7GuZNxTAn0mLFW5HnkP1T3%26tpl%3Dtpl_10085_15730_11224%26l%3D1500117464%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E3%252580%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E6%2525B3%2525A8%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E8%252581%25258C%2525E4%2525B8%25259A%2525E6%25259C%2525BA%2526xp%253Did%28%252522m6c247d9c%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D220%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26oq%3Dwin10%252520python%252520portia%252520%2525E5%2525AE%252589%2525E8%2525A3%252585%26rqlang%3Dcn%26inputT%3D508%26bs%3Dwin10%2520python%2520portia%2520%25E5%25AE%2589%25E8%25A3%2585; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; X_HTTP_TOKEN=5608d432cc526b93496d12c0753a37a0; _gat=1; TG-TRACK-CODE=index_navigation; LGRID=20180122190943-bfbb0b93-ff64-11e7-b4a1-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516619391; SEARCH_ID=335731afdaa945d891544cef0aa75074',
#            #新版cookie
#            # 'Cookie':'adfbid2=0; NTKF_T2D_CLIENTID=guest2472875D-00EA-22A1-F9FE-5670A0BF9C31; __utmv=269921210.|2=Member=369448640=1; _jzqx=1.1519789040.1520577110.1.jzqsr=zhaopin%2Ecom|jzqct=/.-; zg_did=%7B%22did%22%3A%20%2216209775f3017ec-07012130cc0238-4353468-1fa400-16209775f3131%22%7D; dywem=95841923.y; sts_deviceid=164fb2e531e4c0-088b7cb63443b6-47e1039-2073600-164fb2e5320491; diagnosis=0; __zpWAM=1533222478364.169583.1533461678.1533470859.4; rt=fdc293a70d2d4bd293ab98670519e801; smidV2=20180812225224ed58313d5a68d4e927f1dcbb74da676800c04782303b9ec30; LastCity=%E5%85%A8%E5%9B%BD; LastCity%5Fid=489; campusOperateJobUserInfo=7f71310c-3cb8-4a14-8cdb-eaa11566c657; dywec=95841923; __utmc=269921210; zg_08c5bcee6e9a4c0594a5d34b79b9622a=%7B%22sid%22%3A%201534679322962%2C%22updated%22%3A%201534679323167%2C%22info%22%3A%201534513207428%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fxiaoyuan.zhaopin.com%2F%22%7D; urlfrom=121113803; urlfrom2=121113803; adfcid=pzzhubiaoti; adfcid2=pzzhubiaoti; adfbid=0; ZP_OLD_FLAG=false; dywea=95841923.1582933421239342300.1517121651.1534674278.1534679331.23; dywez=95841923.1534679331.23.17.dywecsr=other|dyweccn=121113803|dywecmd=cnt|dywectr=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98; dyweb=95841923.1.10.1534679331; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1533470856,1534426783,1534510238,1534679331; sts_sg=1; sts_sid=16552042f7e13b-0137d20f3a4fc6-2711639-2073600-16552042f7f1bd; zp_src_url=https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fAhw9s0P7KI0KqiAs0Myg-U00000FxNENb00000XL9Z6W.THLyktAJdIjA80K85HRsnj0snjczgv99UdqsusK15yPBuWFBmhfvnj0sn1RYnjb0IHYYPWbkfWPAnjfLwjNDPYuAfYfvnRnLfbmkn1PjnYm3f6K95gTqFhdWpyfqn1D1nW6kPHTYnzusThqbpyfqnHm0uHdCIZwsrBtEILILQMGCmyqspy38mvqV5LPGujYknWDknHn3njnhTv-YuHdsXMGCIyFGmyqYpfKWThnqn1b3njf%26tpl%3Dtpl_11535_17772_13457%26l%3D1505613207%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E5%252587%252586%2525E5%2525A4%2525B4%2525E9%252583%2525A8-%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%252599%2525BA%2525E8%252581%252594%2525E6%25258B%25259B%2525E8%252581%252598%2525E3%252580%252591%2525E5%2525AE%252598%2525E6%252596%2525B9%2525E7%2525BD%252591%2525E7%2525AB%252599%252520%2525E2%252580%252593%252520%2525E5%2525A5%2525BD%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E4%2525B8%25258A%2525E6%252599%2525BA%2525E8%252581%252594%2525E6%25258B%25259B%2525E8%252581%252598%2525EF%2525BC%252581%2526xp%253Did(%252522m3132815743_canvas%252522)%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D83%26ie%3Dutf-8%26f%3D3%26srcqid%3D2315053756065640489%26tn%3D50000022_hao_pg%26wd%3D%25E6%2599%25BA%25E8%2581%2594%25E6%258B%259B%25E8%2581%2598%26oq%3D%25E6%2599%25BA%25E8%2581%2594%25E6%258B%259B%25E8%2581%2598%26rqlang%3Dcn%26sc%3DUWd1pgw-pA7EnHc1FMfqnHR1PjmLrHn1nWmknBuW5y99U1Dznzu9m1YdrjbYrHbsnjc%26ssl_sample%3Ds_4%252Cs_10%252Cs_88%26rsp%3D0; __xsptplusUT_30=1; __utma=269921210.2138135161.1517121651.1534674278.1534679331.25; __utmz=269921210.1534679331.25.17.utmcsr=other|utmccn=121113803|utmcmd=cnt|utmctr=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98; __utmt=1; __utmb=269921210.1.10.1534679331; _jzqa=1.1023953198975836200.1517121651.1533470856.1534679331.15; _jzqc=1; _jzqy=1.1517121651.1534679331.8.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98; _jzqckmp=1; __xsptplus30=30.16.1534679330.1534679330.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23qMN3ItvCU0a6_41Do-H8GNHXqPau78mY%23; _jzqb=1.1.10.1534679331.1; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1534679334; sts_evtseq=8; GUID=a8aa0013680e479caea369738a7200c0; ZL_REPORT_GLOBAL={%22sou%22:{%22actionIdFromSou%22:%22c326424b-7a25-4d7a-952f-5462508abe6a-sou%22%2C%22funczone%22:%22smart_matching%22}}',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#         },
#         'COOKIES_ENABLED': False,
#         'LOG_LEVEL ': 'DEBUG',
#     }
#
#     city_data = {
#         '北京': '530',
#         "上海": "538",
#         "广州": "763",
#         "深圳": "765",
#         "武汉": "736",
#         "成都": "801",
#         "重庆": "551",
#         "郑州": "719",
#         "杭州": "653",
#         "济南": "702",
#         "南京": "635",
#         "西安": "854",
#         "长沙": "749",
#         "哈尔滨": "622",
#         "石家庄": "565",
#         "合肥": "664",
#         "太原": "576",
#         "厦门": "682",
#         "苏州": "639",
#         "天津": "531",
#         "沈阳": "599",
#         "青岛": "703",
#         "无锡": "636",
#         "昆明": "831",
#         "大连": "600",
#         "福州": "681",
#         "长春": "613",
#         "南昌": "691",
#     }
#     search_api = "https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId={}&kw={}&kt=3&sortType=publish"
#     start_api = "https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId={}&kw={}&kt=3&sortType=publish"
#
#     def start_requests(self):
#         for city in CITY:
#             for keyword, filter_kw in KEYWORDS:
#                 city_num = self.city_data[city]
#                 # 访问第一页获取page总数
#                 url = self.start_api.format(city_num, keyword)
#                 yield scrapy.Request(url,self.total_parse,meta={'dt':{"city": city, 'city_num':city_num,"keyword": keyword, "filter":filter_kw}})
#
#     def total_parse(self, response):
#         dt = response.meta['dt']
#         city_num = dt['city_num']
#         keyword = dt['keyword']
#         city = dt['city']
#         filter_kw = dt['filter']
#         data = json.loads(response.text)
#         # 获取总数
#         total = int(data.get('data', {}).get('numFound', 0))
#         # 计算页数
#         pages = total // 60
#         # 遍历每页
#         for i in range(pages + 1):
#             url = self.search_api.format(i * 60, city_num, keyword)
#             yield scrapy.Request(url, self.list_json_parse,
#                                  meta={'dt': {"city": city, "keyword": keyword, "filter": filter_kw}})
#
#     def list_json_parse(self, response):
#         dt = response.meta['dt']
#         data = json.loads(response.text)
#         results = data['data']['results']
#         for result in results:
#             createDate = result['createDate'].split(' ')[0]
#             createDate = int(''.join(createDate.split('-')))
#             updateDate = result['updateDate'].split(' ')[0]
#             updateDate = int(''.join(updateDate.split('-')))
#             yesterday, updatetime = self.yesterday()
#             # 过滤规定周期外的
#             if updateDate >= yesterday:
#                 job_name = result['jobName']
#                 filter_kw = dt['filter']
#                 # 过滤标题不匹配的
#                 for f in filter_kw:
#                     if f.lower() in job_name.lower():
#                         url = result['positionURL']
#                         salary = result['salary']
#                         if 'K' in salary and '-' in salary:
#                             salary = result['salary'].split('-')
#                             salary = '-'.join([str(int(float(i.replace('K', '')) * 1000)) for i in salary])
#                         info = {
#                             'company_name': result['company']['name'],
#                             'company_size': result['company']['size']['name'],
#                             'salary': salary,
#                             'education_background': result['eduLevel']['name'],
#                             'experience': result['workingExp']['name'],
#                             'job_name': job_name,
#                             'category': result['jobType']['display'],
#                             # 'pub_date': result['createDate'].split(' ')[0],
#                             'pub_date': result['updateDate'].split(' ')[0],
#                             'url': url,
#                             'source': 'zl',
#                             'updatetime': updatetime
#
#                         }
#                         dt.update(info)
#                         yield scrapy.Request(url, self.detail_parse, meta={'dt': dt})
#                         break
#
#     def detail_parse(self, response):
#         dt = response.meta['dt'].copy()
#         description = response.xpath('//div[@class="tab-inner-cont"]//text()').extract()
#         description = ''.join(description).replace(' ', '').replace('\n', '').replace('\xa0', ''). \
#             replace('\u3000', '').replace('\r', '').replace('\ufeff\ufeff', ':').split('工作地址：')[0]
#         office_address = response.xpath('//div[@class="tab-inner-cont"]/h2/text()').extract_first() \
#                          or response.xpath(
#             '//span[contains(text(),"公司地址：")]/following-sibling::strong/text()').extract_first()
#         office_address = office_address.replace('\n', '')
#         company_area = response.xpath("//div[@class='company-box']/ul/li[3]/strong//text()").extract_first().replace(
#             '\n', '')
#         filter_kw = ','.join(dt['filter'])
#         number = response.xpath('//span[contains(text(),"招聘人数：")]/following-sibling::strong/text()').extract_first()
#         company_info = response.xpath('//div[@class="tab-inner-cont"][2]//text()').extract()
#         company_info = ''.join(company_info).replace(' ', '').replace('\n', '').replace('\xa0', ''). \
#             replace('\u3000', '').replace('\r', '').replace('\ufeff\ufeff', ':')
#         print(company_info)
#         dt.update(
#             {
#                 'description': description,
#                 'office_address': office_address,
#                 'company_area': company_area,
#                 'filter': filter_kw,
#                 'number': number,
#                 'company_info':company_info
#             }
#         )
#         yield dt
#
#     def yesterday(self, days=DAYS):
#         now = datetime.now()
#         yesterday = now - timedelta(days=days)
#         y = str(yesterday.date())
#         y = y.replace('-', '')
#         return int(y), str(now).split(' ')[0]


# class Zhilian_xiaoyuan_Spider(RedisSpider):
#     '''
#     没有翻页
#     '''
#     name = 'zhilian_xiaoyuan'
#     allowed_domains = ZhilianSpider.allowed_domains
#     redis_key = 'zhilian_xiaoyuan'
#     custom_settings = ZhilianSpider.custom_settings
#     city_data = ZhilianSpider.city_data
#     url = 'https://xiaoyuan.zhaopin.com/full/{num}/{num}_0_0_0_{days}_-1_{kw}_{page}_0'
#
#     def start_requests(self):
#
#         self.days = DAYS
#         if self.days == 7:
#             self.days = 3
#         for city in CITY:
#             city_num = self.city_data[city]
#             for keyword, filter_kw in KEYWORDS:
#                 keyword = keyword.replace('+', '')
#                 dt = {"city": city, 'city_num': city_num, "keyword": keyword, "filter": filter_kw}
#                 yield scrapy.Request(self.url.format(num=city_num, days=self.days, kw=keyword,page=1), self.list_parse,
#                                      meta={'dt': dt})
#
#     def list_parse(self, response):
#         dt = response.meta['dt']
#         filter_kw = dt['filter']
#         li_list = response.xpath('//ul[@class="searchResultListUl"]/li')
#         for li in li_list:
#             job_name = li.xpath('.//p[contains(@class,"searchResultJobName")]/a/text()').extract_first()
#             for fkw in filter_kw:
#                 if fkw.lower() in job_name.lower():
#                     url = 'https:' + li.xpath('.//p[contains(@class,"searchResultJobName")]/a/@href').extract_first()
#                     number = li.xpath('.//em[@class="searchResultJobPeopnum"]/text()').extract_first()
#                     pub_date = li.xpath('.//span[contains(text(),"发布时间：")]//text()').extract()[1]
#                     pub_date = self.date_format(1) if '昨天' in pub_date else pub_date
#                     pub_date = self.date_format(2) if '前天' in pub_date else pub_date
#                     company_name = li.xpath('.//p[@class="searchResultCompanyname"]/span/text()').extract_first()
#                     company_area = li.xpath('.//p[@class="searchResultCompanyIndustry"]/text()').extract_first()
#                     # category = li.xpath('.//span[contains(text(),"职位类别：")]/following-sibling::em/text()').extract_first()
#                     # office_address = li.xpath('.//em[@class="searchResultJobCityval"]/text()').extract_first()
#                     dt.update({
#                         'url': url,
#                         'job_name': job_name,
#                         'number': number,
#                         'pub_date': pub_date,
#                         'company_name': company_name,
#                         'company_area': company_area,
#                         'salary': '',
#                         'experience': "校园招聘",
#                         'education_background': "校园招聘",
#                         # 'office_address': office_address
#                     })
#                     yield scrapy.Request(url, self.detail_parse, meta={'dt': dt})
#                     break
#
#         total = response.xpath('//ul[@id="page"]/li[last()-1]//span/text()').extract_first()
#         print(total)
#         if total:
#             for city in CITY:
#                 for keyword, filter_kw in KEYWORDS:
#                     city_num = self.city_data[city]
#                     for i in range(int(total),1,-1):
#                         print('#########################第{}页###############################'.format(i))
#                         url = self.url.format(num=city_num, days=self.days, kw=keyword,page=i)
#                         print(url)
#                         yield scrapy.Request(url,self.list_parse,meta={'dt':dt})
#
#     def detail_parse(self, response):
#         dt = response.meta['dt'].copy()
#         filter_kw = ','.join(dt['filter'])
#         description = response.xpath('//div[@class="cJob_Detail f14"]//text()').extract()
#         description = ''.join(description).replace(' ', '').replace('\n', '').replace('\xa0', ''). \
#             replace('\u3000', '').replace('\r', '')
#         category = response.xpath('//li[contains(text(),"职位类别：")]/following-sibling::li[1]/text()').extract_first()
#         company_url = 'https://xiaoyuan.zhaopin.com' + response.xpath('//div[@class="cCompanyInfoCon r"]/a/@href').extract_first()
#         dt.update({
#             'description':description,
#             'filter':filter_kw,
#             'category':category
#         })
#         yield scrapy.Request(company_url,self.last_parse,meta={'dt':dt})
#
#     def last_parse(self,response):
#         dt = response.meta['dt'].copy()
#         company_size = response.xpath('//div[@class="cCompanyGuild"]//p[@class="c9"]/span/text()').extract()[1].replace('公司规模：','')
#         office_address = response.xpath('//div[@class="clearfix p20"]/p/text()').extract_first() or dt['city']
#         dt.update({
#             'company_size':company_size,
#             'office_address':office_address.strip()
#         })
#         yield dt
#
#     def date_format(self, days):
#         now = datetime.now()
#         yestoday = now - timedelta(days=days)
#         y = str(yestoday.date())
#         return y

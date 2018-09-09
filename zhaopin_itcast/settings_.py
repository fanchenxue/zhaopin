# -*- coding: utf-8 -*-

# Scrapy settings for zhaopin_itcast project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhaopin_itcast'

SPIDER_MODULES = ['zhaopin_itcast.spiders']
NEWSPIDER_MODULE = 'zhaopin_itcast.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhaopin_itcast (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 80

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'zhaopin_itcast.middlewares.ZhaopinItcastSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
    # 'zhaopin_itcast.proxymiddlewares.ProxyMiddleWare':200,
   # 'zhaopin_itcast.middlewares.ZhaopinItcastDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'zhaopin_itcast.pipelines.ZhaopinItcastPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

COMMANDS_MODULE = 'zhaopin_itcast.commands'

REDIRECT_ENABLED = False

#分布式
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 100
# }
DUPEFILTER_CLASS="scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# REDIS_URL= 'redis://root:Lxcc198#!@47.93.254.164:6379'
# REDIS_URL = 'redis://127.0.0.1:6379'
REDIS_HOST = '47.93.254.164'
# REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PARAMS = { 'password': 'Lxcc198#!', }
SCHEDULER_PERSIST=True
# SCHEDULER_QUEUE_CLASS= "scrapy_redis.queue.SpiderPriorityQueue"
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

###########搜索设置#############
DAYS = 7
CITY = [
    u"北京",
    u"上海",
    u"广州",
    u"深圳",
    u"武汉",
    u"成都",
    u"杭州",
    u"济南",
    u"南京",
    u"西安",

]

KEYWORDS = [
	("java", ["java"]),
	("php", ["php"]),
	(u"前端", [u"前端"]),
	("python", ["python", u"爬虫", u"数据", u"运维", u"测试", "openstack", "web", u"机器学习", u"算法"]),
	(u"测试工程师", [u"测试"]),
]
from scrapy import cmdline
import schedule
from os import system
import time


import os
os.chdir('zhaopin_itcast/spiders')

# cmdline.execute('scrapy runspider zhilian.py'.split())
cmdline.execute('scrapy crawlall'.split())

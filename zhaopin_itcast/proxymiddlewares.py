import time
import requests
import random


class ProxyMiddleWare:
    proxies = [
            # 'http://itcast:Itcast123456@60.185.32.114:9999',
            'http://itcast:Itcast123456@60.185.37.68:9999',
            # 'http://itcast:Itcast123456@60.185.33.154:9999',
            # 'http://itcast:Itcast123456@125.106.83.64:9999'
    ]
    def process_request(self, request, spider):
        # proxy = random.choice(self.proxies)
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy


if __name__ == '__main__':
    pass
    proxies = {
        # 'http': 'http://itcast:Itcast123456@125.106.83.64:9999',
        # 'http': 'http://itcast:Itcast123456@220.185.10.223:9999',
        'http': 'http://itcast:Itcast123456@60.185.37.68:9999',
    }
    res = requests.get('http://www.baidu.com/s?wd=ip', proxies=proxies)
    print(res.text)

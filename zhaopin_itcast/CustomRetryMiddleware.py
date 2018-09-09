from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import random,time
import logging
import zhaopin_itcast.proxymiddlewares


class CustomRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__)
    def delete_proxy(self, proxy):
        if proxy:
            pass
    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            time.sleep(random.randint(3, 5))
            self.logger.warning('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response
# Scrapy settings for batdongsan_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sosanhnha.com_spider'

SPIDER_MODULES = ['sosanhnha_spider.spiders']
NEWSPIDER_MODULE = 'sosanhnha_spider.spiders'
LOG_LEVEL = 'INFO'

FEED_EXPORTERS = {
    'json': 'sosanhnha_spider.exporters.Utf8JsonItemExporter',
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent


# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Cài đặt scrapy-fake-useragent



# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#     'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
#     'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
# }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}


# FAKEUSERAGENT_PROVIDERS = [
#     'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # Sử dụng User-Agent ngẫu nhiên từ thư viện fake_useragent
#     'scrapy_fake_useragent.providers.FakerProvider',  # Sử dụng User-Agent ngẫu nhiên từ Faker
#     'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # Tùy chỉnh User-Agent cố định
# ]



# settings.py

# Cấu hình proxy
# HTTP_PROXY = 'http://43.153.208.148:3128'
HTTP_PROXY = "http://3076a7ba298e91a89c11c6eec6d0650f4c3ce975:@api.zenrows.com:8001"

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# DOWNLOADER_MIDDLEWARES = {
#         'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#         'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#         'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
#         'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
#     }


# Thay thế `your-proxy-server:port` bằng địa chỉ proxy của bạn.

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'

DOWNLOAD_DELAY = 3 
RETRY_TIMES = 5  # Thử lại 5 lần trước khi từ bỏ

COOKIES_ENABLED = True




# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
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
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'batdongsan_spider.middlewares.BatdongsanSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'batdongsan_spider.middlewares.BatdongsanSpiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'batdongsan_spider.pipelines.BatdongsanSpiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

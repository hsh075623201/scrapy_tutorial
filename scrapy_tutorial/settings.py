# -*- coding: utf-8 -*-

# Scrapy settings for news project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

MONGO_URI = 'mongodb://localhost:27017'

BOT_NAME = 'scrapy_tutorial'

SPIDER_MODULES = ['scrapy_tutorial.spiders']
NEWSPIDER_MODULE = 'scrapy_tutorial.spiders'

ITEM_PIPELINES={
    'news.pipelines.MongoPipeline':300,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
}

proxy_list = [
('123.59.83.131', 23128),
('123.59.83.140', 23128),
('123.59.83.137', 23128),
('123.59.83.147', 23128),
('123.59.83.139', 23128),
('123.59.83.132', 23128),
('123.59.83.141', 23128),
('123.59.83.148', 23128),
('123.59.83.130', 23128),
('123.59.83.145', 23128),
('115.28.17.251', 23128),
('121.42.204.43', 23128),
('115.28.203.67', 23128),
('115.28.59.108', 23128),
('139.129.25.112', 23128),
('115.28.102.210', 23128),
('115.28.131.100', 23128),
('115.28.234.179', 23128),
('121.42.158.55', 23128),
('114.215.84.175', 23128),
('139.129.15.129', 23128),
('139.129.13.201', 23128),
('121.42.201.236', 23128),
('115.28.234.20', 23128),
('121.42.29.50', 23128),
('115.28.235.73', 23128),
('120.27.37.30', 23128),
('121.42.158.226', 23128),
('121.42.29.3', 23128),
('115.28.90.223', 23128),
('120.25.147.220', 23128),
('120.25.0.76', 23128),
('120.25.146.18', 23128),
('120.25.147.127', 23128),
('112.74.104.235', 23128),
('120.25.121.118', 23128),
('112.74.107.105', 23128),
('120.25.208.116', 23128),
('120.25.0.159', 23128),
('120.25.0.27', 23128),
('120.25.63.38', 23128),
('120.25.63.26', 23128),
('120.25.62.16', 23128),
('120.25.61.9', 23128),
('120.25.207.39', 23128),
('120.25.147.105', 23128),
('112.74.100.147', 23128),
('120.24.222.208', 23128),
('120.25.61.195', 23128)
]

RANDOMIZE_DOWNLOAD_DELAY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'news.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'news.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'news.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'



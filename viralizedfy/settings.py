BOT_NAME = 'viralizedfy'

SPIDER_MODULES = ['viralizedfy.spiders']

NEWSPIDER_MODULE = 'viralizedfy.spiders'

LOG_LEVEL = 'DEBUG'

ROBOTSTXT_OBEY = False

RETRY_ENABLED = True

RETRY_TIMES = 6

MEDIA_ALLOW_REDIRECTS = True

CONCURRENT_REQUESTS = 64

FILES_STORE = 'foobar'

ITEM_PIPELINES = {
  'viralizedfy.pipelines.PreparePipeline': 100,
  'viralizedfy.pipelines.MimetypePipeline': 200,
  'viralizedfy.pipelines.DownloadPipeline': 300,
  # 'viralizedfy.pipelines.MarkdownifyPipeline': 1000
}

AWS_ACCESS_KEY_ID = 'AKIAS3BUSIV6LMWXD6VG'
AWS_SECRET_ACCESS_KEY = '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'


SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 300,
    'scrapy_magicfields.MagicFieldsMiddleware': 600,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 100,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 300,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 600,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 900
}

MAGIC_FIELDS = {
  'url': "$response:url",
  'spider': '$spider:name',
}

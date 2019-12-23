import os

BOT_NAME = 'viralizedfy'

SPIDER_MODULES = ['viralizedfy.spiders']

NEWSPIDER_MODULE = 'viralizedfy.spiders'

MEDIA_ALLOW_REDIRECTS = True

CONCURRENT_REQUESTS = 64

FILES_STORE = 's3://viralizedfy/'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

ITEM_PIPELINES = {
  'viralizedfy.pipelines.PreparePipeline': 100,
  'viralizedfy.pipelines.MimetypePipeline': 200,
  'viralizedfy.pipelines.DownloadPipeline': 300,
  'viralizedfy.pipelines.MarkdownifyPipeline': 400
}

SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 100,
    'scrapy_magicfields.MagicFieldsMiddleware': 200,
}

DELTAFETCH_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 100,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 200,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 300,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 400
}

MAGIC_FIELDS = {
  'url': "$response:url",
  'spider': '$spider:name',
}

EXTENSIONS = {
  'scrapy_dotpersistence.DotScrapyPersistence': 100
}

DOTSCRAPY_ENABLED = False

ADDONS_AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
ADDONS_AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
ADDONS_S3_BUCKET = 'viralizedfy'

import os

BOT_NAME = 'viralizedfy'
SPIDER_MODULES = ['viralizedfy.spiders']
NEWSPIDER_MODULE = 'viralizedfy.spiders'

MEDIA_ALLOW_REDIRECTS = True

FILES_STORE = os.environ.get('FILES_STORE', 'media')

DOWNLOADER_MIDDLEWARES = {
  'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 100,
  'scrapy.downloadermiddlewares.retry.RetryMiddleware': 200,
  'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 300,
  'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 400
}

ITEM_PIPELINES = {
  'viralizedfy.pipelines.PreparePipeline': 100,
  'viralizedfy.pipelines.TagsPipeline': 200,
  'viralizedfy.pipelines.MimetypePipeline': 300,
  'viralizedfy.pipelines.DownloadPipeline': 400,
}

MAGIC_FIELDS = {
  'url': "$response:url",
  'spider': '$spider:name',
}

SPIDER_MIDDLEWARES = {
  'scrapy_deltafetch.DeltaFetch': 100,
  'scrapy_magicfields.MagicFieldsMiddleware': 200,
}

DELTAFETCH_ENABLED = False

EXTENSIONS = {
  'scrapy_dotpersistence.DotScrapyPersistence': 100
}

DOTSCRAPY_ENABLED = False

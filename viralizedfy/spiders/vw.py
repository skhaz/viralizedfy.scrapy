from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from viralizedfy.items import Entry, EntryLoader


class Spider(CrawlSpider):
  name = 'vw'

  allowed_domains = ['videoswhats.net']

  start_urls = ['https://www.videoswhats.net/']

  rules = (
    Rule(
      LinkExtractor(), callback='parse_item', follow=True
    ),
  )

  def parse_item(self, response):
    loader = EntryLoader(item=Entry(), response=response)
    loader.add_xpath('title', '//*[@class="content"]/h1/text()')
    loader.add_xpath('content', '//*[@class="text"]/*[not(self::span)]/text()')
    loader.add_xpath('media', '//*[@id="object"]/img/@src')
    loader.add_xpath('media', '//*[@id="object"]/video/source/@src')
    loader.add_xpath('poster', '//*[@id="object"]/video/@poster')
    return loader.load_item()

import os
import sys
import re
import hashlib
import mimetypes
import functools
from datetime import datetime
from pathlib import Path
from unicodedata import normalize
from urllib.parse import urlparse

from jinja2 import Environment, BaseLoader, Template

from scrapy.http import Request
from scrapy.utils.python import to_bytes
from scrapy.exceptions import DropItem
from scrapy.exporters import BaseItemExporter
from scrapy.pipelines.files import FilesPipeline

import boto3
import base36


class PreparePipeline():
  def process_item(self, item, spider):
    url = item['url'].encode('utf-8')
    title = item.get('title')
    if title is None:
      raise DropItem(f"No title were found on item: {item}")

    N = 4
    sha256 = hashlib.sha256(url).digest()
    sliced = int.from_bytes(
      memoryview(sha256)[:N].tobytes(), byteorder=sys.byteorder)
    guid = base36.dumps(sliced)

    strip = str.strip
    lower = str.lower
    split = str.split
    deunicode = lambda n: normalize('NFD', n).encode('ascii', 'ignore').decode('utf-8')
    trashout = lambda n: re.sub(r'[\W]+', ' ', n)
    functions = [strip, deunicode, trashout, lower, split]
    fragments = [
      *functools.reduce(
        lambda x, f: f(x), functions, title),
      guid,
    ]

    item.setdefault('content', '')

    item['guid'] = '-'.join(fragments)

    return item


class MimetypePipeline():
  def process_item(self, item, spider):
    media = item.get('media')
    if media is None:
      raise DropItem(f"No media were found on item: {item}")

    mimetype, _ = mimetypes.guess_type(media)
    if mimetype is None:
      raise DropItem(f"Cannot determine the mimetype for media: {media}")
    item['mimetype'] = mimetype

    extension = mimetypes.guess_extension(mimetype)
    if not extension:
      raise DropItem(f"Cannot determine the extension for mimetype: {mimetype}")
    item['extension'] = extension

    title = item.get('title')
    if len(title) < 6
      raise DropItem(f"Invalid title: {title}")
    item['tags'] = [word for word in title.split('-')[:-1] if len(word) > 3]

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(extension)
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    return item


class DownloadPipeline(FilesPipeline):
  def get_media_requests(self, item, info):
    url = item['url']
    filename = ''.join([item['guid'], item['extension']])
    yield Request(url, meta=dict(filename=filename))

  def file_path(self, request, response=None, info=None):
    return request.meta['filename']

  def item_completed(self, results, item, info):
    item['ready'] = bool(results[0][0])
    return item


jinja2_env = Environment(loader=BaseLoader(), trim_blocks=True)

base = Template('''---
title: "{{ title }}"
tags: "[{{ tags }}]"
date: "{{ now }}"
draft: false
---

{{ content }}

''')

tags = '''
![{{ title }}]({{ guid + extension }})
---
`audio: title: {{ guid + extension }}`
---
`video: title: {{ title|tojson }}: {{ guid + extension }}`
'''.split(
  '---'
)

templates = {
  key: f'{{% include base %}}\n{value}'
    for key, value in dict(
      image=tags[0],
      audio=tags[1],
      video=tags[2],
    ).items()
}

class MarkdownifyPipeline():

  def __init__(self, settings, stats):
    self.stats = stats

    url = settings['FILES_STORE']

    self.bucket = urlparse(url).hostname

    self.s3 = boto3.client('s3')

  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings, crawler.stats)

  def process_item(self, item, spider):
    kind, _ = item['mimetype'].split('/')
    template = templates[kind]
    now = datetime.today().strftime('%Y-%m-%d')
    result = jinja2_env.from_string(template).render(base=base, now=now, **item)
    self.s3.put_object(Body=result, Bucket=self.bucket, Key=f'{item["guid"]}.md')

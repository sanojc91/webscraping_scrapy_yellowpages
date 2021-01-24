# -*- coding: utf-8 -*-
import scrapy
import datetime
import socket

from urllib.parse import urlparse, urljoin
from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from yellowpages.items import YellowpagesItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YellowSpider(CrawlSpider):
    name = 'yellow'
    allowed_domains = ['yellowpages.com']
    start_urls = ['https://www.yellowpages.com/search?search_terms=hotels&geo_location_terms=Los+Angeles%2C+CA']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="next ajax-page"]'), ), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="business-name"]'),), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        l = ItemLoader(item=YellowpagesItem(), response=response)
        l.add_xpath('name', '//div[@class="sales-info"]/h1/text()', MapCompose(str.strip, str.title))
        l.add_xpath('phone', '//div[@class="contact"]/p[@class="phone"]/text()', MapCompose(str.strip))
        l.add_xpath('address_line1', '//div[@class="contact"]/h2[@class="address"]/text()', MapCompose(str.strip))
        l.add_xpath('email', './/a[@class="email-business"]/@href', MapCompose(lambda i: urljoin(response.url, i)))
        l.add_xpath('website', './/a[@class="track-visit-website"]/@href', MapCompose(lambda j: urljoin(response.url, j)))

        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()

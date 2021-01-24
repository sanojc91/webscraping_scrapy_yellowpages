# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class YellowpagesItem(scrapy.Item):
    # define the fields for your item here like:
    name = Field()
    phone = Field()
    address_line1 = Field()
    email = Field()
    website = Field()

    # calculated fields
    images = Field()
    location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()


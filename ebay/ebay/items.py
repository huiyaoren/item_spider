# -*- coding: utf-8 -*-

from scrapy import Item, Field


class ListingItem(Item):
    price = Field()
    categories = Field()
    itemLocation = Field()
    shippingOptions = Field()
    seller = Field()
    title = Field()
    conditionId = Field()
    image = Field()
    currentBidPrice = Field()
    buyingOptions = Field()
    condition = Field()
    itemId = Field()
    itemAffiliateWebUrl = Field()
    itemWebUrl = Field()
    itemHref = Field()
    additionalImages = Field()
    data = Field()

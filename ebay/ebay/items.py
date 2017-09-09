# -*- coding: utf-8 -*-

from scrapy import Item, Field


class ListingItem(Item):
    categories = Field()
    itemLocation = Field()
    shippingOptions = Field()
    seller = Field()
    conditionId = Field()
    currentBidPrice = Field()
    buyingOptions = Field()
    condition = Field()
    itemAffiliateWebUrl = Field()
    itemWebUrl = Field()
    itemHref = Field()
    additionalImages = Field()
    time = Field()
    data = Field()

    price = Field()
    country = Field()
    currency = Field()
    itemId = Field()
    startTime = Field()
    viewItemURL = Field()
    categoryID = Field()
    feedbackScore = Field()
    positiveFeedbackPercent = Field()
    newUser = Field()
    registrationDate = Field()
    storeURL = Field()
    quantitySold = Field()
    image = Field()
    hitCount = Field()
    title = Field()
    shipToLocations = Field()
    site = Field()

# -*- coding: utf-8 -*-

from scrapy import Item, Field


class ListingItem(Item):
    currency = Field()                  # 商品货币类型
    category = Field()                  # 商品分类
    date = Field()                      # 商品爬取日期
    hitCount = Field()                  # 商品访问量
    itemURL = Field()                   # 商品页面链接
    itemLocation = Field()              # 商品所在地
    itemId = Field()                    # 商品 id
    imageURL = Field()                  # 商品图片链接
    shipToLocations = Field()           # 商品发货地区
    site = Field()                      # 商品所属站点
    startTime = Field()                 # 商品上架时间
    price = Field()                     # 商品价格
    quantitySold = Field()              # 商品历史销量
    title = Field()                     # 商品标题

    sellerRegistrationDate = Field()    # 卖家注册时间
    sellerFeedbackScore = Field()       # 卖家评价反馈评分
    sellerFeedbackPercentage = Field()  # 卖家好评率
    sellerName = Field()                # 卖家用户名

    data = Field()

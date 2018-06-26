# item_spider


## 关于 item_spider

> 一个基于 spider-redis 的分布式爬虫

架构设计: https://www.jianshu.com/p/cd4054bbc757


## Spider

商品详情爬虫

    detail_json_redis_spider.py
    
    detail_xml_redis_spider.py

商品列表爬虫

    listing_redis_spider.py
    
    listing_spider.py
    
    listing_xml_redis_spider.py


## Script

    category.py - 分类数据预处理 

    dumper.py - 数据库备份 

    dustman.py - 数据库备份清理 

    monitor.py - 爬虫数据监控 

    recognizer.py - 图形验证码识别 

    register.py - 自动化注册 

    statistician.py - 数据统计 

## Pipeline

    CleanPipeline - 数据清洗
    
    MongodbPipeline - MongoDB 写入
    
    MysqlPipeline - Mysql 写入
    
    NewItemPipeline - 新上架商品写入
    
    HotItemPipeline - 热销商品写入
    
    ShopStatisticsPipeline - 店铺信息统计

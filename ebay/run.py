def run():
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    process.crawl('item_spider')
    process.start()


if __name__ == '__main__':
    run()




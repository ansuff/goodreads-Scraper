BOT_NAME = 'book_review_scraper'

SPIDER_MODULES = ['book_review_scraper.spiders']
NEWSPIDER_MODULE = 'book_review_scraper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'book_review_scraper.pipelines.SQLitePipeline': 300,
}

FEED_FORMAT = 'csv'
FEED_URI = 'data/%(name)s.csv'
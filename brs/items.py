import scrapy

class BookItem(scrapy.Item):
    genre = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    rating = scrapy.Field()
    num_ratings = scrapy.Field()
    num_reviews = scrapy.Field()
    description = scrapy.Field()
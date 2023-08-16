import scrapy
from ..items import BookItem

class GoodreadsSpider(scrapy.Spider):
    """
    This code uses Scrapy to scrape the Goodreads website for information about
    the most popular books in a variety of genres. It uses the BookItem class
    defined in items.py to store the information. It stores the scraped data in
    a JSON file called books.json.

    Scrapy is a Python library for scraping websites. It works by defining
    "spiders" that specify how to scrape the data from a website. A spider is a
    class that subclasses scrapy.Spider. The GoodreadsSpider class is a spider
    that scrapes the Goodreads website. The parse() method is the starting point
    for the spider. It starts by scraping the most popular books in each of the
    genres listed in the genres variable. The parse_genre() method is called once
    for each genre. It scrapes the most popular books in that genre. For each
    book, the parse_book() method is called. It scrapes information about that
    book and stores it in a BookItem instance. The parse_book() method returns
    the BookItem instance. The spider stores the BookItem instances in a JSON
    file called books.json using the FEEDS setting in settings.py.
    """

    name = 'goodreads'
    allowed_domains = ['goodreads.com']
    start_urls = [
        'https://www.goodreads.com/shelf/show',
        'https://www.goodreads.com/genres/most_read',
    ]

    genres = ['Science Fiction', 'Travel', 'Thriller', 'Poetry', 'Fantasy', 'Business']

    def parse(self, response):
        """
        Parse the most popular books in each genre.
        """
        for genre in self.genres:
            genre_url = response.css(f'a[href*="{genre}"]::attr(href)').get()
            yield response.follow(genre_url, callback=self.parse_genre, meta={'genre': genre})  # noqa: E501

    def parse_genre(self, response):
        """
        Parse the most popular books in a genre.
        """
        genre = response.meta['genre']
        # if response contains shelf/show, extract only top 30 books
        if response.url.startswith('https://www.goodreads.com/shelf/show'):
            for book in response.css('.left')[:30]:
                book_url = book.css('a::attr(href)').get()
                yield response.follow(book_url, callback=self.parse_book, meta={'genre': genre})  # noqa: E501
        for book in response.css('.coverWrapper'):
            book_url = book.css('a::attr(href)').get()
            yield response.follow(book_url, callback=self.parse_book, meta={'genre': genre})  # noqa: E501

    def parse_book(self, response):
        """
        Parse a book.
        """
        genre = response.meta['genre']
        title = response.css('h1#bookTitle::text').get().strip()
        author = response.css('a.authorName span::text').get().strip()
        rating = response.css('span[itemprop="ratingValue"]::text').get()
        num_ratings = response.css('meta[itemprop="ratingCount"]::attr(content)').get()
        num_reviews = response.css('meta[itemprop="reviewCount"]::attr(content)').get()
        description = response.css('div#description span[style="display:none"]::text').get()  # noqa: E501
        yield BookItem(
            genre=genre,
            title=title,
            author=author,
            rating=rating,
            num_ratings=num_ratings,
            num_reviews=num_reviews,
            description=description,
        )
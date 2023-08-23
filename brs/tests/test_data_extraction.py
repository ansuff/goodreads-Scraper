import unittest
from unittest.mock import patch
from brs.data_extraction import GoodreadsScraper


class TestGoodreadsScraper(unittest.TestCase):
    @patch('brs.data_extraction.webdriver.Chrome')
    def test_extract_book_data(self, mock_driver):
        # Set up the mock driver
        mock_driver.return_value.page_source = """
            <html>
                <head><title>Book Title</title></head>
                <body>
                    <h1>Book Title</h1>
                    <span class="ContributorLink__name">Author Name</span>
                    <span data-testid="reviewsCount">100 reviews</span>
                    <span data-testid="ratingsCount">4 ratings</span>
                    <div class="RatingStatistics__rating">4.5 stars</div>
                    <span class="Formatted">Book description</span>
                </body>
            </html>
        """
        # Create a GoodreadsScraper instance
        scraper = GoodreadsScraper()

        # Call the extract_book_data method with a mock URL
        book_data = scraper.extract_book_data('https://www.goodreads.com/book/show/1234')

        # Check that the book data was extracted correctly
        self.assertEqual(book_data['title'], 'Book Title')
        self.assertEqual(book_data['author'], 'Author Name')
        self.assertEqual(book_data['reviews'], 100)
        self.assertEqual(book_data['ratings'], 4)
        self.assertEqual(book_data['stars'], 4.5)
        self.assertEqual(book_data['description'], 'Book description')
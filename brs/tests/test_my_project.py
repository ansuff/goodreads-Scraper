import unittest
from unittest.mock import patch, MagicMock
from brs.data_extraction import GoodreadsScraper


class TestGoodreadsScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = GoodreadsScraper()

    @patch('requests.get')
    def test_extract_book_data(self, mock_get):
        # Mock the response from the book page
        mock_response = MagicMock()
        mock_response.content = b'<html><body><h1 data-testid="bookTitle">Title</h1><span class="ContributorLink__name">Author</span><span data-testid="reviewsCount">100 reviews</span><span data-testid="ratingsCount">4 avg rating</span><div class="RatingStatistics__rating">4.5</div><span class="Formatted">Description</span></body></html>'  # noqa: E501
        mock_get.return_value = mock_response

        # Call the extract_book_data method with a mock URL
        book_data = self.scraper.extract_book_data('https://www.goodreads.com/book/show/1234')

        # Check that the book data was extracted correctly
        self.assertEqual(book_data['title'], 'Title')
        self.assertEqual(book_data['author'], 'Author')
        self.assertEqual(book_data['reviews'], 100)
        self.assertEqual(book_data['ratings'], 4)
        self.assertEqual(book_data['stars'], 4.5)
        self.assertEqual(book_data['description'], 'Description')

    @patch('requests.get')
    def test_extract_most_read_books_genre_data(self, mock_get):
        # Mock the response from the genre page
        mock_response = MagicMock()
        mock_response.content = b'<html><body><div class="coverWrapper"><a href="/book/show/1234"></a></div><div class="coverWrapper"><a href="/book/show/5678"></a></div></body></html>'  # noqa: E501
        mock_get.return_value = mock_response

        # Mock the extract_book_data method to return a fixed book data dictionary
        self.scraper.extract_book_data = MagicMock(return_value={
            'title': 'Title',
            'author': 'Author',
            'reviews': 100,
            'ratings': 4,
            'stars': 4.5,
            'description': 'Description'
        })

        # Call the extract_genre_data method with a mock genre
        book_data = self.scraper.extract_genre_data('fiction',url='https://www.goodreads.com/genres/most_read', max_books=-1, page_class='coverWrapper')  # noqa: E501

        # Check that the book data was extracted correctly
        self.assertEqual(len(book_data), 1)
        self.assertEqual(book_data.iloc[0]['genre'], 'fiction')
        self.assertEqual(book_data.iloc[0]['book_id'], '1234')
        self.assertEqual(book_data.iloc[0]['title'], 'Title')
        self.assertEqual(book_data.iloc[0]['author'], 'Author')
        self.assertEqual(book_data.iloc[0]['reviews'], 100)
        self.assertEqual(book_data.iloc[0]['ratings'], 4)
        self.assertEqual(book_data.iloc[0]['stars'], 4.5)
        self.assertEqual(book_data.iloc[0]['description'], 'Description')

    @patch('requests.get')
    def test_extract_top_books_genre_data(self, mock_get):
        # Mock the response from the genre page
        mock_response = MagicMock()
        mock_response.content = b'<html><body><div class="coverWrapper"><a href="/book/show/1234"></a></div><div class="coverWrapper"><a href="/book/show/5678"></a></div></body></html>'  # noqa: E501
        mock_get.return_value = mock_response

        # Mock the extract_book_data method to return a fixed book data dictionary
        self.scraper.extract_book_data = MagicMock(return_value={
            'title': 'Title',
            'author': 'Author',
            'reviews': 100,
            'ratings': 4,
            'stars': 4.5,
            'description': 'Description'
        })

        # Call the extract_genre_data method with a mock genre
        book_data = self.scraper.extract_genre_data('fiction',url='https://www.goodreads.com/shelf/show', max_books=-1, page_class='coverWrapper')  # noqa: E501

        # Check that the book data was extracted correctly
        self.assertEqual(len(book_data), 1)
        self.assertEqual(book_data.iloc[0]['genre'], 'fiction')
        self.assertEqual(book_data.iloc[0]['book_id'], '1234')
        self.assertEqual(book_data.iloc[0]['title'], 'Title')
        self.assertEqual(book_data.iloc[0]['author'], 'Author')
        self.assertEqual(book_data.iloc[0]['reviews'], 100)
        self.assertEqual(book_data.iloc[0]['ratings'], 4)
        self.assertEqual(book_data.iloc[0]['stars'], 4.5)
        self.assertEqual(book_data.iloc[0]['description'], 'Description')
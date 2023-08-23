import sqlite3

import pandas as pd

from brs.data_extraction import GoodreadsScraper
from brs.data_storage import GoodreadsStorage

# how many books do you want to extract
MAX_BOOKS_MOST_READ = -1 # the max! -1 means all
MAX_BOOKS_TOP_BOOKS = 30

# Define the URLs to extract the data from
# for now it is the books on shelves
TOP_BOOKS_URL = 'https://www.goodreads.com/shelf/show'


def main():
    """
    Extracts book data from Goodreads and stores it in a SQLite database.
    
    The genres to extract are defined in the genres list. The data is extracted
    using the GoodreadsScraper class and stored in a pandas DataFrame. The data
    is then uploaded to a SQLite database using the GoodreadsStorage class.
    """
    # Define the genres to extract
    genres = ['Science Fiction', 'Travel', 'Thriller', 'Poetry', 'Fantasy', 'Business']  # noqa: E501
    # Extract the book data for each genre
    scraper = GoodreadsScraper()
    most_read_url = 'https://www.goodreads.com/genres/most_read'
    most_read_books = pd.concat([scraper.extract_genre_data(
        genre,url=most_read_url,max_books=MAX_BOOKS_MOST_READ, page_class='coverWrapper' # noqa: E501
        ) for genre in genres], ignore_index=True)
    top_books = pd.concat([scraper.extract_genre_data(
        genre,url=TOP_BOOKS_URL,max_books=MAX_BOOKS_TOP_BOOKS, page_class='left'
        ) for genre in genres], ignore_index=True)
    # Create a SQLite database
    with sqlite3.connect('data/books.db') as conn:
        storage = GoodreadsStorage(conn)
        storage.create_schema()
        storage.upload_data(most_read_books=most_read_books, top_books=top_books)

if __name__ == '__main__':
    main()
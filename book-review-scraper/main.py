import sqlite3
import pandas as pd
from data_extraction import GoodreadsScraper
from data_storage import GoodreadsStorage

def main():
    """
    Extracts book data from Goodreads and stores it in a SQLite database.
    
    The genres to extract are defined in the genres list. The data is extracted
    using the GoodreadsScraper class and stored in a pandas DataFrame. The data
    is then uploaded to a SQLite database using the GoodreadsStorage class.
    """
    # Define the genres to extract
    genres = ['Science Fiction', 'Travel', 'Thriller', 'Poetry', 'Fantasy', 'Business']
    # Extract the book data for each genre
    scraper = GoodreadsScraper()
    data = pd.concat([scraper.extract_genre_data(genre) for genre in genres], ignore_index=True)
    data.to_csv('data/books.csv', index=False)
    # Create a SQLite database
    with sqlite3.connect('data/books.db') as conn:
        storage = GoodreadsStorage(conn)
        storage.create_schema()
        storage.upload_data(data)

if __name__ == '__main__':
    main()
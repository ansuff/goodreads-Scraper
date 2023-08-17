import unittest
import sqlite3
import pandas as pd
from brs.data_storage import GoodreadsStorage

class TestGoodreadsStorage(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.conn = sqlite3.connect(':memory:')
        self.storage = GoodreadsStorage(self.conn)
        self.storage.create_schema()
        
        # Define test data
        self.top_books = pd.DataFrame({
            'genre': ['Science Fiction', 'Travel', 'Thriller'],
            'author': ['Author 1', 'Author 2', 'Author 3'],
            'title': ['Book 1', 'Book 2', 'Book 3'],
            'reviews': [100, 200, 300],
            'ratings': [44, 35, 40],
            'stars': [4.5, 3.5, 4.0],
            'description': ['Description 1', 'Description 2', 'Description 3']
        })
        
        self.most_read_books = pd.DataFrame({
            'genre': ['Poetry', 'Fantasy', 'Business'],
            'author': ['Author 4', 'Author 5', 'Author 6'],
            'title': ['Book 4', 'Book 5', 'Book 6'],
            'reviews': [400, 500, 600],
            'ratings': [45, 35, 40],
            'stars': [4.5, 3.5, 4.0],
            'description': ['Description 4', 'Description 5', 'Description 6']
        })
        
    def tearDown(self):
        # Close the database connection
        self.conn.close()
        
    def test_create_schema(self):
        # Check that the tables exist in the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        self.assertIn(('genres',), tables)
        self.assertIn(('authors',), tables)
        self.assertIn(('top_books',), tables)
        self.assertIn(('most_read_books',), tables)
        
    def test_upload_data(self):
        # Upload the test data to the database
        self.storage.upload_data(self.most_read_books, self.top_books)
        
        # Check that the data was uploaded correctly
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM genres;')
        self.assertEqual(cursor.fetchone()[0], 6)
        cursor.execute('SELECT COUNT(*) FROM authors;')
        self.assertEqual(cursor.fetchone()[0], 6)
        cursor.execute('SELECT COUNT(*) FROM top_books;')
        self.assertEqual(cursor.fetchone()[0], 3)
        cursor.execute('SELECT COUNT(*) FROM most_read_books;')
        self.assertEqual(cursor.fetchone()[0], 3)
        
    def test_upload_data_duplicate_data(self):
        # Add a duplicate row to the test data
        duplicate_row = pd.DataFrame({
            'genre': ['Science Fiction'],
            'author': ['Author 1'],
            'title': ['Book 1'],
            'reviews': [100],
            'ratings': [4.5],
            'stars': [4.5],
            'description': ['Description 1']
        })
        top_books = pd.concat([self.top_books, duplicate_row])
        
        # Upload the test data to the database
        self.storage.upload_data(self.most_read_books, top_books)
        
        # Check that the duplicate row was not inserted into the database
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM top_books WHERE title = "Book 1";')
        self.assertEqual(cursor.fetchone()[0], 1)
        
    def test_upload_data_missing_data(self):
        # Add a row with missing data to the test data
        missing_row = pd.DataFrame({
            'genre': ['Science Fiction'],
            'author': ['Author 1'],
            'title': ['Book 4'],
            'reviews': [100],
            'ratings': [4.5],
            'stars': [4.5],
            'description': [None]
        })
        top_books = pd.concat([self.top_books, missing_row])
        
        # Upload the test data to the database
        with self.assertRaises(sqlite3.IntegrityError):
            self.storage.upload_data(self.most_read_books, top_books)
        #self.storage.upload_data(self.most_read_books, top_books)
        
        # Check that the missing data was not inserted into the database
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM top_books WHERE description IS NULL;')
        self.assertEqual(cursor.fetchone()[0], 0)
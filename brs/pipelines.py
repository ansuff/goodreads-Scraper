import sqlite3

class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('../data/books.db')
        self.create_schema()

    def close_spider(self, spider):
        self.conn.close()

    def create_schema(self):
        with open('../data/schema.sql', 'r') as f:
            schema = f.read()
        self.conn.executescript(schema)

    def process_item(self, most_read_books, top_books, spider):
        self.conn.execute(
            'INSERT INTO top_books (genre, title, author, rating, num_ratings, num_reviews, description)'  # noqa: E501
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (top_books['genre'], top_books['title'], top_books['author'], top_books['rating'], top_books['num_ratings'], top_books['num_reviews'], top_books['description'])  # noqa: E501
        )
        self.conn.execute(
            'INSERT INTO most_read_books (genre, title, author, rating, num_ratings, num_reviews, description)'  # noqa: E501
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (most_read_books['genre'], most_read_books['title'], most_read_books['author'], most_read_books['rating'], most_read_books['num_ratings'], most_read_books['num_reviews'], most_read_books['description'])  # noqa: E501
        )
        self.conn.commit()
        return top_books,most_read_books
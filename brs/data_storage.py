class GoodreadsStorage:
    def __init__(self, conn):
        self.conn = conn
    
    def create_schema(self):
        """
        Create the database schema if it does not exist.

        The schema consists of four tables:
        - genres: contains the genres of the books
        - authors: contains the authors of the books
        - top_books: contains the top books on the site (shelves)
        - most_read_books: contains the most read books this week on the site
        """
        # Define the database schema
        schema = '''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS top_books (
            genre_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            reviews INTEGER NOT NULL,
            ratings INTEGER NOT NULL,
            stars REAL NOT NULL,
            description TEXT NOT NULL,
            PRIMARY KEY (title, author_id, genre_id)
            FOREIGN KEY (genre_id) REFERENCES genres (id),
            FOREIGN KEY (author_id) REFERENCES authors (id)
        );

        CREATE TABLE IF NOT EXISTS most_read_books (
            genre_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            reviews INTEGER NOT NULL,
            ratings INTEGER NOT NULL,
            stars REAL NOT NULL,
            description TEXT NOT NULL,
            PRIMARY KEY (title, author_id, genre_id)
            FOREIGN KEY (genre_id) REFERENCES genres (id),
            FOREIGN KEY (author_id) REFERENCES authors (id)
        );
        '''
        # Create the database schema
        with self.conn:
            self.conn.executescript(schema)

    def upload_data(self, most_read_books, top_books):
        """
        Upload the data to the SQLite database.

        The data is uploaded in two steps:
        - Insert the genres into the genres table
        - Insert the top books on the site into the top_books table
        - Insert the most read books this week into the most_read_books table
        """
        # Insert the genres into the genres table
        genres = set(top_books['genre'].unique()) | set(most_read_books['genre'].unique()) # noqa: E501
        authors = set(top_books['author'].unique()) | set(most_read_books['author'].unique())  # noqa: E501
        with self.conn:
            for i, genre in enumerate(genres):
                # only insert the genres that are not already in the table
                if not self.conn.execute('SELECT * FROM genres WHERE name = ?', (genre,)).fetchone():  # noqa: E501
                    self.conn.execute('INSERT INTO genres (id, name) VALUES (?, ?)', (i+1, genre)) # noqa: E501
        with self.conn:
            for i, author in enumerate(authors):
                # only insert the authors that are not already in the table
                if not self.conn.execute('SELECT * FROM authors WHERE name = ?', (author,)).fetchone():  # noqa: E501
                    self.conn.execute('INSERT INTO authors (id, name) VALUES (?, ?)', (i+1, author))  # noqa: E501
        # Insert the books into the books table
        with self.conn:
            for _, row in top_books.iterrows():
                genre_id = self.conn.execute('SELECT id FROM genres WHERE name = ?', (row['genre'],)).fetchone()[0]  # noqa: E501
                author_id = self.conn.execute('SELECT id FROM authors WHERE name = ?', (row['author'],)).fetchone()[0]  # noqa: E501
                # Check if the book already exists in the table
                if not self.conn.execute('SELECT * FROM top_books WHERE title = ? AND author_id = ? AND genre_id = ?', (row['title'], author_id, genre_id)).fetchone(): # noqa: E501
                    self.conn.execute(
                        'INSERT INTO top_books (genre_id, author_id, title, reviews, ratings, stars, description)' # noqa: E501
                        'VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (genre_id, author_id, row['title'], row['reviews'], row['ratings'], row['stars'], row['description']) # noqa: E501
                    )
            for _, row in most_read_books.iterrows():
                genre_id = self.conn.execute('SELECT id FROM genres WHERE name = ?', (row['genre'],)).fetchone()[0]  # noqa: E501
                author_id = self.conn.execute('SELECT id FROM authors WHERE name = ?', (row['author'],)).fetchone()[0]  # noqa: E501
                if not self.conn.execute('SELECT * FROM top_books WHERE title = ? AND author_id = ? AND genre_id = ?', (row['title'], author_id, genre_id)).fetchone(): # noqa: E501
                    self.conn.execute(
                        'INSERT INTO most_read_books (genre_id, author_id, title, reviews, ratings, stars, description)' # noqa: E501
                        'VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (genre_id, author_id, row['title'], row['reviews'], row['ratings'], row['stars'], row['description']) # noqa: E501
                    )
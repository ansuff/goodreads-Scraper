class GoodreadsStorage:
    def __init__(self, conn):
        self.conn = conn
    
    def create_schema(self):
        """
        Create the database schema if it does not exist.

        The schema consists of two tables:
        - genres: contains the genres of the books
        - books: contains the books and their information
        """
        # Define the database schema
        schema = '''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS top_books (
            book_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            reviews INTEGER NOT NULL,
            ratings INTEGER NOT NULL,
            stars REAL NOT NULL,
            description TEXT NOT NULL,
            PRIMARY KEY (book_id, genre_id),
            FOREIGN KEY (genre_id) REFERENCES genres (id)
        );

        CREATE TABLE IF NOT EXISTS most_read_books (
            book_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            reviews INTEGER NOT NULL,
            ratings INTEGER NOT NULL,
            stars REAL NOT NULL,
            description TEXT NOT NULL,
            PRIMARY KEY (book_id, genre_id),
            FOREIGN KEY (genre_id) REFERENCES genres (id)
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
        genres = top_books['genre'].unique()
        with self.conn:
            for i, genre in enumerate(genres):
                # only insert the genres that are not already in the table
                if not self.conn.execute('SELECT * FROM genres WHERE name = ?', (genre,)).fetchone():  # noqa: E501
                    self.conn.execute('INSERT INTO genres (id, name) VALUES (?, ?)', (i+1, genre)) # noqa: E501
        # Insert the books into the books table
        with self.conn:
            for _, row in top_books.iterrows():
                for genre in row['genre'].split(','):
                    genre_id = genres.tolist().index(genre.strip()) + 1
                    self.conn.execute(
                        'INSERT INTO top_books (book_id, genre_id, title, author, reviews, ratings, stars, description)' # noqa: E501
                        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        (row['book_id'], genre_id, row['title'], row['author'], row['reviews'], row['ratings'], row['stars'], row['description']) # noqa: E501
                    )
            for _, row in most_read_books.iterrows():
                for genre in row['genre'].split(','):
                    genre_id = genres.tolist().index(genre.strip()) + 1
                    self.conn.execute(
                        'INSERT INTO most_read_books (book_id, genre_id, title, author, reviews, ratings, stars, description)' # noqa: E501
                        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        (row['book_id'], genre_id, row['title'], row['author'], row['reviews'], row['ratings'], row['stars'], row['description']) # noqa: E501
                    )
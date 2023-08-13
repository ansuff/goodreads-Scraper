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

        CREATE TABLE IF NOT EXISTS books (
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

    def upload_data(self, data):
        """
        Upload the data to the SQLite database.

        The data is uploaded in two steps:
        - Insert the genres into the genres table
        - Insert the books into the books table
        """
        # Insert the genres into the genres table
        genres = data['genre'].unique()
        with self.conn:
            for i, genre in enumerate(genres):
                # only insert the genres that are not already in the table
                if not self.conn.execute('SELECT * FROM genres WHERE name = ?', (genre,)).fetchone():
                    self.conn.execute('INSERT INTO genres (id, name) VALUES (?, ?)', (i+1, genre))
        # Insert the books into the books table
        with self.conn:
            for _, row in data.iterrows():
                for genre in row['genre'].split(','):
                    genre_id = genres.tolist().index(genre.strip()) + 1
                    self.conn.execute('INSERT INTO books (book_id, genre_id, title, author, reviews, ratings, stars, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                                      (row['book_id'], genre_id, row['title'], row['author'], row['reviews'], row['ratings'], row['stars'], row['description']))
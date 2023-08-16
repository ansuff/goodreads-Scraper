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
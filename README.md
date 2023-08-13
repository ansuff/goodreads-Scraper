# Book Reviews Scraper

This project extracts the top 30 books read this week on Goodreads in six different genres: Science Fiction, Travel, Thriller, Poetry, Fantasy, and Business. The extracted data is then stored in a SQLite database. This project is useful for anyone who wants to keep track of the most popular books in these genres and analyze trends in reading habits. It can also be used as a starting point for building a recommendation system or for conducting data analysis on book trends.


## Installation

To install the project and its dependencies, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the `run.sh` script to install Poetry and the project dependencies.

```bash
./run.sh poetry
```

4. Run the run.sh script to scrape the top 30 books from Goodreads and store them in a SQLite database.
   
```bash
./run.sh scrap-store
```

5. (Optional) Run the run.sh script to run the project tests.

```bash 
./run.sh test-project
```
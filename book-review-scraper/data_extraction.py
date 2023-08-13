import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


class GoodreadsScraper:
    def __init__(self):
        self.base_url = 'https://www.goodreads.com'
    
    def extract_book_data(self, url):
        """
        Extracts the book data from a book page on Goodreads
        
        Parameters:
        url (str): The URL of the book page

        Returns:
        dict: A dictionary containing the book data containing
        the following details: title, author, reviews, ratings, stars, description
        """
        #print(f'Extracting book data from {url}')
        start_time = time.time()
        while True:
            # Send a GET request to the book page
            response = requests.get(url)
            # Parse the HTML content of the book page
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1', {'data-testid': 'bookTitle'})
            if title is not None:
                title = title.text.strip()
            author = soup.find('span', class_='ContributorLink__name')
            if author is not None:
                author = author.text.strip()
            reviews = soup.find('span', attrs={'data-testid': 'reviewsCount'})
            if reviews is not None:
                reviews = int(reviews.text.split()[0].replace(',', ''))
            ratings = soup.find('span', attrs={'data-testid': 'ratingsCount'})
            if ratings is not None:
                ratings = int(ratings.text.split()[0].replace(',', ''))
            stars = soup.find('div', class_='RatingStatistics__rating')
            if stars is not None:
                stars = float(stars.text.split()[0])
            description = soup.find('span', class_='Formatted')
            if description is not None:
                description = description.text.strip()
            # Check if any of the extracted data is None
            if (title is not None and author is not None and reviews is not None and
                ratings is not None and stars is not None and description is not None):
                # Return the extracted data as a dictionary
                return {
                    'title': title,
                    'author': author,
                    'reviews': reviews,
                    'ratings': ratings,
                    'stars': stars,
                    'description': description
                }
            time.sleep(5)
            # Check if the timeout has been exceeded
            elapsed_time = time.time() - start_time
            if elapsed_time > 300:
                print(f'Timeout exceeded for {url}')
                return {
                    'title': title,
                    'author': author,
                    'reviews': reviews,
                    'ratings': ratings,
                    'stars': stars,
                    'description': description
                }

    def extract_genre_data(self, genre):
        """
        Extracts the top 30 books read this week for a given genre
        and extracts the book data for each book

        Parameters:
        genre (str): The genre to extract the book data for

        Returns:
        pd.DataFrame: A DataFrame containing the book data for the genre
        """
        genre_url_format = f'https://www.goodreads.com/genres/most_read/{genre}'
        # Extract the book URLs for the genre
        book_urls = []
        url = genre_url_format.format(genre=genre.lower().replace(' ', '-'))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        book_urls += [self.base_url + book.find('a')['href']
                       for book in soup.find_all('div', class_='coverWrapper')][:30]
        # Extract the book data for each book URL
        book_data = []
        print(f'Proceed to extract top 30 book data for genre: {genre}')
        for book_url in book_urls:
            book_id = re.search(r'\d+', book_url).group()
            book_data_item = self.extract_book_data(book_url)
            book_data.append({'genre': genre, 'book_id': book_id, **book_data_item})
        # Return the extracted book data as a DataFrame
        print(f'Extracted top {len(book_data)} books read this week for genre {genre}')
        return pd.DataFrame(book_data)
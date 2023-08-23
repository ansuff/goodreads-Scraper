import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class GoodreadsScraper:
    def __init__(self):
        self.base_url = 'https://www.goodreads.com'
        options = webdriver.ChromeOptions()
        service = Service()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        
        self.driver = webdriver.Chrome(service=service, options=options)

    def extract_book_data(self, url):
        """
        Extracts the book data from a book page on Goodreads
        
        Parameters:
        url (str): The URL of the book page

        Returns:
        dict: A dictionary containing the book data containing
        the following details: title, author, reviews, ratings, stars, description
        """
        self.driver.get(url)
        time.sleep(1) # Wait for the page to load
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        title = soup.find('h1')
        author = soup.find('span', class_='ContributorLink__name')
        reviews = soup.find('span', attrs={'data-testid': 'reviewsCount'})
        ratings = soup.find('span', attrs={'data-testid': 'ratingsCount'})
        stars = soup.find('div', class_='RatingStatistics__rating')
        description = soup.find('span', class_='Formatted')
        # Check if any of the extracted data is None
        if (title is not None and author is not None and reviews is not None and
            ratings is not None and stars is not None and description is not None):
            title = title.text.strip()
            author = author.text.strip()
            reviews = int(reviews.text.split()[0].replace(',', ''))
            ratings = int(ratings.text.split()[0].replace(',', ''))
            stars = float(stars.text.split()[0])
            description = description.text.strip()
            # Return the extracted data as a dictionary
            return {
                'title': title,
                'author': author,
                'reviews': reviews,
                'ratings': ratings,
                'stars': stars,
                'description': description
            }
        else:
            print(f'Failed to extract book data for {url}, returning None')
            return None

    def extract_genre_data(self, genre, url, max_books=30, page_class='left'):
        """
        Extracts the top 30 books read this week for a given genre
        and extracts the book data for each book

        Parameters:
        genre (str): The genre to extract the book data for

        Returns:
        pd.DataFrame: A DataFrame containing the book data for the genre
        """
        genre_url_format = url + f'/{genre}'
        # Extract the book URLs for the genre
        book_urls = []
        url = genre_url_format.format(genre=genre.lower().replace(' ', '-'))
        self.driver.get(url)
        time.sleep(1) # Wait for the page to load
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        book_urls += [self.base_url + book.find('a')['href']
                       for book in soup.find_all('div', class_=page_class)] [:max_books]
                       # for most read class = 'coverWrapper'
        # Extract the book data for each book URL
        book_data = []
        if max_books == -1:
            print(f'Proceed to extract most read books data for genre: {genre}\n')
        else:
            print(f'Proceed to extract top {max_books} books data for genre: {genre}\n')
        for book_url in book_urls:
            book_data_item = self.extract_book_data(book_url)
            if book_data_item is not None:
                book_data.append({'genre': genre, **book_data_item})
        # Return the extracted book data as a DataFrame
        if max_books == -1:
            print(f'\nExtracted most read books this week for genre {genre}')
        else:
            print(f'\nExtracted top {max_books} books genre {genre}')
                
        self.driver.quit()
        return pd.DataFrame(book_data)
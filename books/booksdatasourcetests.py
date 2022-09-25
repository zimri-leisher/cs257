'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source_small = BooksDataSource('smalldatasource.csv')
        self.data_source_large = BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source_small.authors('Three')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Author', 'Three'))

    def test_authors_case_insensitivity(self):
        authors = self.data_source_small.authors('five')
        authors_lowercase = self.data_source_small.authors('FIVE')
        self.assertEqual(authors, authors_lowercase)
    
    def test_authors_no_search_text(self):
        all_authors = self.data_source_small.authors(None)
        for author in [Author('Author', 'One'), Author('Author', 'Two'), Author('Author', 'Three'), Author('Author', 'Four'), Author('Author', 'Five')]:
            self.assertTrue(author in all_authors)

    def test_authors_sorted_surname(self):  
        authors = self.data_source_small.authors(None)
        self.assertEqual(authors[0].surname, 'Five')
        self.assertEqual(authors[0].given_name, 'AAthor')
        self.assertEqual(authors[1].surname, 'Five')
        self.assertEqual(authors[1].given_name, 'Author')
        self.assertEqual(authors[2].surname, 'Four')
        self.assertEqual(authors[3].surname, 'One')
        self.assertEqual(authors[4].surname, 'Three')
        self.assertEqual(authors[5].surname, 'Two')

    def test_authors_bad_input(self):
        with self.assertRaises(TypeError):
            self.data_source_large.authors(True)

    def test_unique_book(self):
        books = self.data_source_large.books('Blackout')
        self.assertTrue(len(books) == 1)
        self.assertTrue(authors[0] == Book('Blackout'))

    def test_books_case_insensitivity(self):
        books_lowercase = self.data_source_large.books('emma')
        books_uppercase = self.data_source_large.books('EMMA')
        self.assertEqual(books_lowercase, books_uppercase)

    def test_books_no_search_text(self):
        books = self.data_source_small.books(None)
        actual_books = [Book('One', 100, Author('Author', 'One')), Book('Two', 100, Author('Author', 'One')), Book('Three', 200, Author('Author', 'Two')), Book('Three', 200, Author('Author', 'Three')), Book('Three', 201, Author('Author', 'Two')), Book('Four', 300, Author('Author', 'Four')), Book('"Five "', 400, Author('Author', 'Four')), Book('Six ', 500, Author('Author', 'Five')), Book('Seven', 600, Author('AAthor', 'Five'))]
        for book in actual_books:
            self.assertTrue(book in books) 

    def test_books_sorted_by_year(self):
        books = self.data_source_small.books(None, 'year')
        self.assertEqual(books[0].year, 100)
        self.assertEqual(books[0].title, 'One')
        self.assertEqual(books[1].publication_year, 100)
        self.assertEqual(books[1].title, 'Two')
        self.assertEqual(books[2].publication_year, 200)
        self.assertEqual(books[3].publication_year, 200)
        self.assertEqual(books[4].publication_year, 201)
        self.assertEqual(books[5].publication_year, 300)
        self.assertEqual(books[6].publication_year, 400)
        self.assertEqual(books[7].publication_year, 500)
        self.assertEqual(books[8].publication_year, 600)

    def test_books_sorted_by_title(self):
        books = self.data_source_small.books(None, 'title')
        self.assertEqual(books[0].title, '"Five "')
        self.assertEqual(books[1].title, 'Four')
        self.assertEqual(books[2].title, 'One')
        self.assertEqual(books[3].title, 'Seven')
        self.assertEqual(books[4].title, 'Six ')
        self.assertEqual(books[5].title, 'Three')
        self.assertEqual(books[6].title, 'Three')
        self.assertEqual(books[7].title, 'Three')
        self.assertEqual(books[8].title, 'Two')
        

    def test_books_default_sort(self):
        books = self.data_source_small.books(None)
        self.assertEqual(self.data_source_small.books('title'), books) 


    def test_books_btn_yrs_inclusive(self):
        books = self.data_source_small.books_between_years(300, 301)
        self.assertEqual(books[0].title, 'Four')
        
        books = self.data_source_small.books_between_years(299, 300)
        self.assertEqual(books[0].title, 'Four')

    
    def test_sort_publication_year(self):
        books = self.data_source_small.books_between_years(400, 600)
        self.assertEqual(books[0].title, '"Five "')
        self.assertEqual(books[1].title, 'Six ')
        self.assertEqual(books[2].title, 'Seven')

    def test_books_btn_yrs_break_ties(self):
        books = self.data_source_small.books_between_years(100,100)
        self.assertEqual(books[0].title, 'One')
        self.assertEqual(books[1].title, 'Two')

    def test_books_btn_yrs_start_yr_none(self):
        books = self.data_source_small.books_between_years(None, 200)
        self.assertEqual(books[0].title, 'One')
        self.assertEqual(books[1].title, 'Two')
        self.assertEqual(books[2].title, 'Three')
        self.assertEqual(books[3].title, 'Three')

    def test_books_btn_yrs_end_yr_none(self):
        books = self.data_source_small.books_between_years(500, None)
        self.assertEqual(books[0].title, 'Six')
        self.assertEqual(books[1].title, 'Seven')

    def test_books_btn_yrs_both_none(self):
        books = self.data_source_small.books_between_years(None, None)
        self.assertEqual(len(books), 9)


 
if __name__ == '__main__':
    unittest.main()


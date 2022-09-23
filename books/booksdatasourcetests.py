'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    # authors
    # test case insensitivity
    # test search_text=None
    # test sorted by surname
    # test sorted by surname breaking ties
    # test non-string input
    

    def test_authors_case_insensitivity(self):
        authors = self.data_source.authors('Pratchett')
        authors_lowercase = self.data_source.authors('pratchett')
        self.assertEqual(authors, authors_lowercase)
    
    def test_authors_no_search_text(self):
        small_data_source = BooksDataSource('smalldatasource.csv')
        all_authors = small_data_source.authors(None)
        #... assert the authors match

    def test_authors_sorted_surname(self):  
        small_data_source = BooksDataSource('smalldatasource.csv')
        authors = small_data_source.authors(None)
        #... assert that the authors are sorted by surname
        authors = self.data_source.authors('b')
        #... assert that the authors are sorted by surname
        # and test breaking ties by given name

    def test_authors_bad_input(self):
        with self.assertRaises(TypeError):
            self.data_source.authors(True)

    def test_unique_book(self):
        books = self.data_source.books('Blackout')
        self.asserTrue(len(books) == 1)
        self.assertTrue(authors[0] == Book('Blackout')

    def test_books_case_insensitivity(self):
        books_lowercase = self.data_source.books('emma')
        books_uppercase = self.data_source.books('EMMA')
        self.assertEqual(books_lowercase, books_uppercase)

    def test_books_no_search_text(self):
        small_data_source = BooksDataSource('smalldatasource.csv')
        books = small_data_source.books(None)
        # ... test that the books are right size, right order, etc

    def test_books_sorted_by_year(self):
        pass

    def test_books_sorted_by_title(self):
        pass
 
    #books
    # test case insensitivity
    # test serach text = NOne
    #test sorted by year
    # test sorted by title
if __name__ == '__main__':
    unittest.main()


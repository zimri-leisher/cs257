#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2022

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''

import csv
import re


class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        self.authors_list = []
        self.books_list = []
        with open(books_csv_file_name) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                #Splits if there multiple authors
                author_description = row[2].split(' and ')
                for authors in author_description:
                    #Splits into name, birthyear, and deathyear
                    authors = re.split('[(-]', authors)
                    author_name = authors[0].split()
                    first_name = ""
                    #Case for 2-part first names
                    if len(author_name) > 2:
                        surname = author_name[-1]
                        for i in range(len(author_name) - 1):
                            first_name = first_name + author_name[i] + " "
                        #remove whitespaces on right side
                        first_name = first_name.rstrip()
                    else:
                        first_name = author_name[0]
                        surname = author_name[1]
                    birth_year = authors[1]
                    death_year = authors[2].replace(')', '')
                    death_year = death_year if death_year != "" else None
                    
                    self.authors_list.append(Author(surname, first_name, birth_year, death_year))
                    self.books_list.append(Book(row[0], row[1]))

        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        pass


    def authors(self, search_text=None):
        authors_search = []
        for author in self.authors_list:
            if search_text in (author.given_name + " " + author.surname):
                authors_search.append(author)
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        return authors_search

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        filtered_books = []
        for book in self.books_list:
            
        return filtered_books

    def books_between_years(self, start_year=None, end_year=None):
        
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        return []

def main():
    BooksDataSource('/Users/zackdong/Documents/CS257/cs257-zimri/books/smalldatasource.csv')
    # parse the args
    # start with the full list of books
    # for each filter (title, author, date)
    #   remove books from the full list which don't match the filter
    # sort by the specified sorting method (in the args)
    # for each book remaining 

if __name__ == "__main__":
    main()
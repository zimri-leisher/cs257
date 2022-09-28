#!/usr/bin/env python3
"""
    booksdatasource.py
    Jeff Ondich, 21 September 2022

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
"""

import csv
import re
from argparse import ArgumentParser
from typing import List


class Author:
    def __init__(self, given_name="", surname="", birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        """ For simplicity, we're going to assume that no two authors have the same name. """
        return self.surname == other.surname and self.given_name == other.given_name

    def __str__(self):
        return f"{self.given_name} {self.surname} ({self.birth_year}-{self.death_year if self.death_year else ''})"


class Book:
    def __init__(self, title="", publication_year=None, authors=None):
        """ Note that the self.authors instance variable is a list of
            references to Author objects. """
        if authors is None:
            authors = []
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        """ We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". """
        return self.title == other.title

    def __str__(self):
        return f"Book({self.title}, {self.publication_year}, " + "".join([str(author) for author in self.authors]) + ")"


def _get_books_from_csv(csv_file):
    books_list = []
    with open(csv_file) as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            # Splits if there are multiple authors
            authors = []
            for author_description in row[2].split(" and "):
                # Splits into name, birthyear, and deathyear
                author_description = re.split("[(-]", author_description)
                author_name = author_description[0].split()
                first_name = ""
                # Case for 2-part first names
                if len(author_name) > 2:
                    surname = author_name[-1]
                    for i in range(len(author_name) - 1):
                        first_name = first_name + author_name[i] + " "
                    # remove whitespaces on right side
                    first_name = first_name.rstrip()
                else:
                    first_name = author_name[0]
                    surname = author_name[1]
                birth_year = author_description[1] if len(author_description) > 1 else None
                death_year = author_description[2].replace(")", "") if len(author_description) > 2 else None
                death_year = death_year if death_year != "" else None
                authors.append(Author(first_name, surname, birth_year, death_year))
            books_list.append(Book(row[0], int(row[1]), authors))
    return books_list


def _get_authors_from_books(books):
    authors = []
    for book in books:
        for author in book.authors:
            if author not in authors:
                authors.append(author)
    return authors


class BookFilter:
    def check(self, book) -> bool:
        pass


class TitleFilter(BookFilter):

    def __init__(self, title):
        self.title = title

    def check(self, book) -> bool:
        return not self.title or self.title.lower() in book.title.lower()


class AuthorFilter(BookFilter):

    def __init__(self, author_match_str):
        self.author_match_str = author_match_str

    def check(self, book) -> bool:
        return not self.author_match_str or any([
            self.author_match_str.lower() in (author.given_name + " " + author.surname).lower()
            for author in book.authors])


class PublicationYearFilter(BookFilter):

    def __init__(self, start_year, end_year):
        self.start_year = int(start_year) if start_year else None
        self.end_year = int(end_year) if end_year else None

    def check(self, book) -> bool:
        if self.start_year and int(book.publication_year) < self.start_year:
            return False
        if self.end_year and int(book.publication_year) > self.end_year:
            return False
        return True


class CompoundFilter(BookFilter):

    def __init__(self, filters):
        self.filters = filters

    def check(self, book) -> bool:
        return all([f.check(book) for f in self.filters])


class BooksDataSource:
    def __init__(self, books_data):
        """ The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        """
        self.all_books = []
        if isinstance(books_data, str):
            # books_data is a csv file path
            self.all_books = _get_books_from_csv(books_data)
        elif isinstance(books_data, list):
            self.all_books = books_data
        else:
            raise Exception("Invalid argument passed to BooksDataSource: " + books_data)
        self.all_authors = _get_authors_from_books(self.all_books)

    def authors(self, search_text=None):
        """ Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        """
        filtered = []
        for author in self.all_authors:
            if not search_text or search_text.lower() in (author.given_name + " " + author.surname).lower():
                filtered.append(author)
        filtered = sorted(filtered, key=lambda a: a.given_name)
        filtered = sorted(filtered, key=lambda a: a.surname)
        return filtered

    def books(self, search_text=None, sort_by="title"):
        """ Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        """
        filtered = self.filter(TitleFilter(search_text))
        if sort_by == "title":
            # first sort by publication year, and then title so that the publication years break ties
            filtered = sorted(filtered, key=lambda b: int(b.publication_year))
            filtered = sorted(filtered, key=lambda b: b.title.lower())
        else:
            # first sort by title, and then publication year so that the title breaks ties
            filtered = sorted(filtered, key=lambda b: b.title.lower())
            filtered = sorted(filtered, key=lambda b: int(b.publication_year))
        return filtered

    def books_between_years(self, start_year=None, end_year=None):
        """ Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        """
        filtered = self.filter(PublicationYearFilter(start_year, end_year))
        filtered = sorted(filtered, key=lambda b: b.title.lower())
        filtered = sorted(filtered, key=lambda b: int(b.publication_year))
        return filtered

    def filter(self, book_filter: BookFilter) -> List[Book]:
        return list(filter(book_filter.check, self.all_books))



# Zimri Leisher and Zach Dong
# September 2022

from argparse import ArgumentParser

from booksdatasource import *


def main():
    arg_parse = ArgumentParser()
    # arg_parse.add_argument("-h", "--help", help="Print usage message", action="store_true")
    arg_parse.add_argument("-i", "--input", help="Loads books from the CSV file INPUT.",
                           type=str, default="books.csv")
    arg_parse.add_argument("-t", "--title", help="Filters results to books whose title matches TITLE.",
                           type=str)
    arg_parse.add_argument("-a", "--author", help="Filters results to books whose author's name matches AUTHOR.",
                           type=str)
    arg_parse.add_argument("-d", "--date",
                           help="In the format START_YEAR[,END_YEAR]. Filters results to books whose start year is "
                                "after START_YEAR inclusive, and before END_YEAR inclusive, if it is specified",
                           type=str)
    arg_parse.add_argument("-s", "--sort", help="SORT = title|date. "
                                                "Sorts the results by either the title or the date published.",
                           type=str, default="title")
    arg_parse.add_argument("-o", "--output",
                           help="Specifies the output format for the results. "
                                "This string can consist of any combination of 0 or 1 of the following characters: "
                                "'a', 't', 'd', which correspond to printing the author, title and date published "
                                "respectively. For example, if --output dt is passed in, the output for each book "
                                "matching the filters will be the date published followed by the title.",
                           type=str, default="tad")
    args = arg_parse.parse_args()
    filters = []
    if args.title:
        filters.append(TitleFilter(args.title))
    if args.author:
        filters.append(AuthorFilter(args.author))
    if args.date:
        start_year, *end_year = [s.replace("(", "").replace(")", "").replace(" ", "") for s in args.date.split(",")]
        start_year = int(start_year)
        end_year = int(end_year[0]) if len(end_year) > 0 and end_year[0] != '' else None
        filters.append(PublicationYearFilter(start_year, end_year))
    for c in args.output:
        if c not in ['a', 't', 'd']:
            raise Exception("Invalid format character " + c + ", valid characters are 'a', 't', 'd'")
    compound_filter = CompoundFilter(filters)
    data = BooksDataSource(args.input)
    matching = data.filter(compound_filter)
    if args.sort == "title":
        matching = sorted(matching, key=lambda b: b.publication_year)
        matching = sorted(matching, key=lambda b: b.title)
    elif args.sort == "date":
        matching = sorted(matching, key=lambda b: b.title)
        matching = sorted(matching, key=lambda b: b.publication_year)
    else:
        raise Exception("Invalid sort type " + args.sort)
    for book in matching:
        formatted_book = []
        for format_char in args.output:
            if format_char == 'a':
                formatted_book.append(", ".join([str(author) for author in book.authors]))
            elif format_char == 't':
                formatted_book.append(str(book.title))
            elif format_char == 'd':
                formatted_book.append(str(book.publication_year))
        print(", ".join(formatted_book))


if __name__ == "__main__":
    main()

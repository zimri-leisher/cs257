# zimri leisher, 20 october 2022
import sys
import psycopg2
from argparse import ArgumentParser
import config


def get_connection():
    """Returns a connection to the olympics SQL database"""
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()


def get_athletes(noc):
    """Returns a list of all athletes who competed for the given NOC"""
    connection = get_connection()
    cursor = connection.cursor()

    query = """SELECT DISTINCT people.name FROM people, nocs, performances WHERE performances.person = people.id AND performances.noc = nocs.id AND nocs.noc = %s"""

    cursor.execute(query, (noc, ))
    return list(cursor)


def get_gold_medals():
    """Returns a list of NOCs mapped to the number of gold medals their athletes have won, sorted by decreasing number of gold medals"""
    connection = get_connection()
    cursor = connection.cursor()

    query = """SELECT DISTINCT nocs.noc, COUNT(medals.medal_type) FROM performances, nocs, medals WHERE performances.noc = nocs.id AND medals.medal_type = 'Gold' AND medals.performance = performances.id GROUP BY nocs.noc ORDER BY COUNT(medals.medal_type) DESC;"""

    cursor.execute(query)
    return list(cursor)


def get_people(games):
    """Returns a list of athletes who competed in the games with the given year"""
    connection = get_connection()
    cursor = connection.cursor()

    query = """SELECT people.name, people.sex FROM people, performances, games WHERE people.id = performances.person AND games.year = %s AND games.id = performances.game"""

    cursor.execute(query, (int(games), ))
    return list(cursor)


def display_data(data):
    """Loops over a list of tuples and displays each entry, separated by commas, on a new line"""
    for row in data:
        for key in row:
            print(str(key), end=", ")
        print()


def main():
    # honestly, i feel like this CLI is kinda pointless. it's basically just a wrapper for some SQL commands
    # all useful functionality i can think of basically boils down to "implement sql syntax but on the
    # command line"
    # so i'm just going to follow the words of the instructions and not the spirit, by implementing
    # subcommands
    arg_parse = ArgumentParser()
    subparsers = arg_parse.add_subparsers(dest="subparser_name")
    athletes_parser = subparsers.add_parser("athletes", help="Lists all athletes that ever competed for a given NOC")
    athletes_parser.add_argument("noc", nargs="+", help="The NOC to get all the athletes of")
    medals_parser = subparsers.add_parser("medals", help="Lists all gold medals won by NOC in descending order of number of medals")
    competitors_parser = subparsers.add_parser("competitors", help="Lists all competitors in a given games year")
    competitors_parser.add_argument("games", nargs="+", help="The games year to list all competitors in")
    args = arg_parse.parse_args()
    
    if not args.subparser_name:
        arg_parse.print_help()
        arg_parse.error("Must pick a subcommand")
    elif args.subparser_name == "athletes":
        if len(args.noc) != 1:
            arg_parse.error("Can only specify one athlete")
        athletes = get_athletes(args.noc[0])
        display_data(athletes)
    elif args.subparser_name == "medals":
        medals = get_gold_medals()
        display_data(medals)
    elif args.subparser_name == "competitors":
        if len(args.games) != 1:
            arg_parse.error("Can only specify one games year")
        people = get_people(args.games[0])
        display_data(people)



if __name__ == "__main__":
    main()

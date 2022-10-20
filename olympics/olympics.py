import sys
import psycopg2
from argparse import ArgumentParser
import config

# want the user to be able to:
# print usage statement
# list names of all athletes from a noc
# list all nocs and the number of gold medals they've won, in decreasing order of the number of gold medals
# one more operation of your choosing

def get_connection():
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def main():
    connection = get_connection()



if __name__ == "__main__":
    main()

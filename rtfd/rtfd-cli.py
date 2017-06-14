from bs4 import BeautifulSoup
#from colorama import init, Fore, Style
import requests
import json
import argparse

# parse positional and optional arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description='Download docs right from the Command-Line')

    parser.add_argument(
        'query',
        metavar='QUERY',
        type=str,
        nargs='*',
        help='name of the project')
#    parser.add_argument(
#        '-n',
#        '--no-color',
#        help='do not colorize or style text',
#        action='store_true')

    return parser

# parse the query into a searchable query
def generate_search_query(query):
    query = (' '.join(query)).replace(' ', '+')
    return query


# the main function
def rtfd(query):
    query = generate_search_query(query)




def command_line():
    parser = parse_args()

    init(autoreset=True)

    query = args.query   
    rtfd(query)



if __name__ == '__main__':

    command_line()

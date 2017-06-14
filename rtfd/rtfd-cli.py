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

# returns all titles from the search page
def title_scraper(query):
    project_titles = []
    url = 'https://readthedocs.org/search/?q='+str(query)+'&version=latest&type=project&language=en'
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    for p in soup.find_all('p', {'class': 'module-item-title'}):
        for a in p.find_all('a'):
            title = a.string
            project_titles.append(title)
    return project_titles

#converts titles into project names
def decode_title(result):
    result = result.lower()
    result = result.replace(" ","-")
    return result

#prints first 10 project titles
def show_project_titles(result,numb):
    print(str(numb)+'.'+str(result))    

#returns list of 10 project_names
def ten_titles(all_titles):
    names = []
    numb = 1
    for result in all_titles[:10]:
        name = decode_title(result)
        show_project_titles(result ,numb)
        numb += 1
        names.append(name)
    return names

#Collects inputs from the user and returns selected project name
def get_project_input(names):
    while True:
        selection = int(input('> '))
        if selection <= len(names) and selection >= 1:
            break
        else:
            print("Choose a valid number!!")    
    return names[selection -1]

#returns links of available docs
def links_scraper(selected_project):
    url = 'http://readthedocs.org/api/v1/project/'+str(selected_project)+'?format=json'
    json_obj = requests.get(url).text
    data = json.loads(json_obj)
    for k, v in data['downloads'].items():
        print(k, "-->", v)

# the main function
def rtfd(query):
    query = generate_search_query(query)
    all_titles = title_scraper(query)
    req_projects_names =  ten_titles(all_titles)
    
    print("\nChoose required project:")
    selected_project = get_project_input(req_projects_names)

    print("\nAvailable Formats:\n")
    available_links = links_scraper(selected_project) 

def command_line():
    parser = parse_args()
    args = parser.parse_args()
    query = args.query   
    rtfd(query)

if __name__ == '__main__':

    command_line()

from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from tqdm import tqdm
from .helpers import formatstr
import requests
import json
import argparse
import os

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
    parser.add_argument(
        '-o',
        '--output-directory',
        type=str,
        nargs=1,
        help='custom output directory'
        )
    parser.add_argument(
        '-c',
        '--color',
        help='colorize or style text',
        action='store_true')
    return parser

# parse the query into a searchable query
def generate_search_query(query):
    query = (' '.join(query)).replace(' ', '+')
    return query

# returns all titles from the search page
def title_scraper(query):
    project_titles = []                                                         #list of all project titles from search results
    project_descs = []
    url = 'https://readthedocs.org/search/?q='+str(query)+'&version=latest&type=project&language=en'
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    for p in soup.find_all('li', {'class': 'module-item'}):
        ps = p.find_all('p')
        if not ps:
            formatstr("No results found.", RED, colored)
            exit()
        try:
            title_p, desc_p, *_ = ps
        except ValueError:
            # some results have no description
            title_p = ps[0]
            desc = 'Description not available.'
        else:
            desc = desc_p.get_text()
            desc = decode_description(desc)

        title = title_p.find('a').string
        project_titles.append(title)
        project_descs.append(desc)
    return project_titles, project_descs

#converts titles into project names
def decode_title(result):
    result = result.lower()
    result = result.replace(" ","-").replace("_","-")
    return result

#house keeping for description
def decode_description(result):
    result = result.strip()
    result = result.replace('=','').replace('\r','').replace('\n','').replace('...','')
    return result

#prints first 10 project names with description
def display_projects(result,numb,desc):
    string = str(numb)+'> '+str(result)
    formatstr(string, CYAN, colored)
    formatstr(desc, BLUE, colored)
    print()

#returns list of 10 project names with description
def ten_projects(all_titles, all_descs):
    names = []                          #project name list
    numb = 1
    print('\n')
    for result, desc in zip(all_titles[:10], all_descs[:10]):
        name = decode_title(result)
        display_projects(result ,numb, desc)
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

#prints list of available file formats to download
def show_available_formats(file_types,numb):
    string = str(numb)+'.'+str(file_types)
    formatstr(string, CYAN, colored)

#returns links of available docs
def links_scraper(selected_project):
    file_types = []
    download_links = []
    numb = 1
    url = 'http://readthedocs.org/api/v1/project/'+str(selected_project)+'?format=json'
    json_obj = requests.get(url).text
    data = json.loads(json_obj)
    for k, v in data['downloads'].items():
        file_types.append(k)
        download_links.append(v)
    for result in file_types:
        show_available_formats(result,numb)
        numb += 1
    return download_links

#Collects inputs from the user and returns selected file's link
def get_file_input(download_links):
    while True:
        selection = int(input('> '))
        if selection <= len(download_links) and selection >= 1:
            break
        else:
            print("Choose a valid number!!")
    return download_links[selection -1]

# makes dir input workable
def generate_dir_query(dir):
    dir = ' '.join(dir)
    return dir

#downloads the required file
def download_file(selected_file,dir):
    json_url = 'https:' + str(selected_file)
    r = requests.get(json_url, allow_redirects=True, stream=True)           # to get content after redirection
    total_size = int(r.headers.get('content-length', 0));                   # Total size in bytes.
    file_url = r.url                                                        #redirected url
    file_name = file_url.split('/')[-1]
    if dir:                                                                 #if custom dir is mentioned
        dir = generate_dir_query(dir)
        string = "Directory =" + dir
        formatstr(string, MAGENTA, colored)
        if not os.path.exists(dir):                                         #Create directory is not exists
            os.makedirs(dir)
            string = "Created directory "+dir
            formatstr(string, MAGENTA, colored)
        print(GREEN)
        with open(dir+file_name, 'wb') as f:
          for data in tqdm(r.iter_content(), total=total_size, unit='B', unit_scale=True):
            f.write(data)
        print(u"\u2713 " + str(file_name) + " has been downloaded.\n" + Style.RESET_ALL)
    else:
        print(GREEN)
        with open(file_name, 'wb') as f:
            for data in tqdm(r.iter_content(), total=total_size, unit='B', unit_scale=True):
                f.write(data)
        print(u"\u2713" + str(file_name) + " has been downloaded.\n" + Style.RESET_ALL)

# the main function
def rtfd(query,dir):
    query = generate_search_query(query)
    all_titles, all_descs = title_scraper(query)
    req_projects_names =  ten_projects(all_titles, all_descs)
    print("\nChoose required project:")
    selected_project = get_project_input(req_projects_names)
    print("\nAvailable Formats:\n")
    download_links = links_scraper(selected_project)
    print("\nChoose format you wish to download:")
    selected_file = get_file_input(download_links)
    print("\nDownloading the selected format, please wait......\n")
    download_file(selected_file, dir)

def command_line():
    init()
    parser = parse_args()
    args = parser.parse_args()
    if not args.query:
        parser.print_help()
        exit()
    query = args.query                      #user query
    dir = args.output_directory             #custom user dir
    global colored
    colored = args.color                    #colorize the text
    rtfd(query,dir)

#GLOBAL VARIABLES
CYAN = Fore.CYAN + Style.BRIGHT             #list of colors to choose from
GREEN = Fore.GREEN + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
MAGENTA = Fore.MAGENTA + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT

if __name__ == '__main__':
    command_line()

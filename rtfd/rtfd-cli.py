from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import requests
import json
import argparse
import os
from tqdm import tqdm

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
    project_titles = []                                    #list of all project titles from search results
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
def show_project_titles(result,numb,colored=False): 
    if colored:        
        print(Fore.CYAN + Style.BRIGHT + str(numb)+'.'+str(result) + Style.RESET_ALL)
    else:
        print(str(numb)+'.'+str(result))

#returns list of 10 project_names
def ten_titles(all_titles, colored):
    names = []                          #project name list
    numb = 1
    print('\n')
    for result in all_titles[:10]:
        name = decode_title(result)
        if colored:
            show_project_titles(result ,numb, colored)
        else:
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

#prints list of available file formats to download
def show_available_formats(file_types,numb, colored=False):
    if colored:
        print(Fore.CYAN + Style.BRIGHT + str(numb)+'.'+str(file_types) + Style.RESET_ALL)
    else:
        print(str(numb)+'.'+str(file_types))

#returns links of available docs
def links_scraper(selected_project, colored):
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
        show_available_formats(result,numb,colored)
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
def download_file(selected_file,dir, colored=False):
    json_url = 'https:' + str(selected_file)
    r = requests.get(json_url, allow_redirects=True, stream=True)  # to get content after redirection     
    total_size = int(r.headers.get('content-length', 0));   # Total size in bytes.    
    file_url = r.url                            #redirected url
    file_name = file_url.split('/')[-1]
    if colored:
        if dir:                                 #if custom dir is mentioned
            dir = generate_dir_query(dir)
            print(Fore.MAGENTA + Style.BRIGHT + "Directory =" + dir + Style.RESET_ALL)
            if not os.path.exists(dir):         #Create directory is not exists
                os.makedirs(dir)
                print(Fore.MAGENTA + Style.BRIGHT +"Created directory "+dir + Style.RESET_ALL)
            print(Fore.GREEN + Style.BRIGHT) 
            with open(dir+file_name, 'wb') as f:
                for data in tqdm(r.iter_content(), total=total_size, unit='B', unit_scale=True):    
                    f.write(data)
            print(str(file_name) + " has been downloaded.")
        else:
            print(Fore.GREEN + Style.BRIGHT) 
            with open(file_name, 'wb') as f:
                for data in tqdm(r.iter_content(), total=total_size, unit='B', unit_scale=True):
                    f.write(data)
            print(str(file_name) + " has been downloaded." + Style.RESET_ALL)
    else:
        if dir:                                 #if custom dir is mentioned
            dir = generate_dir_query(dir)
            print("Directory =" + dir)
            if not os.path.exists(dir):         #Create directory is not exists
                os.makedirs(dir)
                print("Created directory "+dir)
            with open(dir+file_name, 'wb') as f:
                for data in tqdm(r.iter_content(), total=total_size, unit='B', unit_scale=True):    
                    f.write(data)                   
            print(str(file_name) + " has been downloaded.")
        else: 
            with open(file_name, 'wb') as f:
                for data in tqdm(r.iter_content(), total=total_size, unit='B', unit_scale=True):
                    f.write(data)
            print(str(file_name) + " has been downloaded.")                  
   

# the main function
def rtfd(query,dir,colored):
    query = generate_search_query(query)
    all_titles = title_scraper(query)
    req_projects_names =  ten_titles(all_titles, colored)    
    print("\nChoose required project:")
    selected_project = get_project_input(req_projects_names)
    print("\nAvailable Formats:\n")
    download_links = links_scraper(selected_project, colored)
    print("\nChoose format you wish to download:")
    selected_file = get_file_input(download_links)
    print("\nDownloading the selected format, please wait......\n")
    download_file(selected_file, dir ,colored)    

def command_line():
    parser = parse_args()
    args = parser.parse_args()
    init()
    if not args.query:
        parser.print_help()
        exit()
    query = args.query                      #user query
    dir = args.output_directory             #custom user dir
    colored = args.color                    #colorize the text
    rtfd(query,dir,colored)

if __name__ == '__main__':
    command_line()

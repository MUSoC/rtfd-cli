import requests
import json
from bs4 import BeautifulSoup


# parse the query into a searchable query

def generate_search_query(query):
    query = query.replace(' ', '+')
    return query

def pname_grabber(string):
    pname_list = []
    query = generate_search_query(string)
    url = 'https://readthedocs.org/search/?q=' + str(query) + '&version=latest&type=project&language=en'
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code,'html.parser')
    for p in soup.find_all('p',{'class':'module-item-title'}):
        for a in p.find_all('a'):
            project_titles = a.string
            project_links = 'https://readthedocs.org' + str(a.get('href'))
            #print(project_titles)
            #print(project_links)
            project_name =  project_titles.lower()
            project_name = project_name.replace(' ','-')
            print(project_name)
            download_links(project_name)
            pname_list.append(project_name)
    return pname_list

# grabs links to the available doc files using api v1
def download_links(project_name):
    url = 'http://readthedocs.org/api/v1/project/'+str(project_name)+'?format=json'
    json_obj = requests.get(url).text
    data = json.loads(json_obj)
    for k, v in data['downloads'].items():
        print(k, "-->", v)

pname_grabber("django")



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
            #print(project_name)
            pname_list.append(project_name)
    return pname_list



list = pname_grabber("django")
print(list)

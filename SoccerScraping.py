__author__ = 'agr70'

import requests
from bs4 import BeautifulSoup
import pandas as pd


class SoccerScraping:


    def __init__(self, url, base_url):
        self.url = url
        self.data = pd.DataFrame()
        self.teams = {}
        self.base_url = base_url

        #inicializamos el html
        page = requests.get(URL, verify=False)
        self.soup = BeautifulSoup(page.content, "html.parser")


    def find_teams(self):
        # obtenemos la grid de los equipos
        teams_grid = self.soup.find(id="stats_squads_standard_for").find('tbody')
        # obtenemos la lista de los equipos
        teams_list = teams_grid.find_all('tr')
        teams_list_clean = []
        teams_urls = []
        for team in teams_list:
            team_link = team.find('a')
            team_link = str(team_link)
            
            string_ind_ini = team_link.index('">') + 2
            string_ind_end = team_link.index('a>') - 2
            team_clean = team_link[string_ind_ini:string_ind_end]
            teams_list_clean.append(team_clean)
            
            string_url_ini = team_link.index('href="') + 6
            string_url_end = team_link.index('>') - 1
            team_url = team_link[string_url_ini:string_url_end]
            teams_urls.append(team_url)
            
        teams_dict = dict(zip(teams_list_clean, teams_urls))
        print(teams_dict)







URL = "https://fbref.com/es/comps/12/Estadisticas-de-La-Liga/"
base_url = 'https://fbref.com/'
soccer_scraping = SoccerScraping(URL, base_url)
soccer_scraping.find_teams()
#buscamos los equipos

#print(page.text)

#results = soup.find(id="ResultsContainer")

#print(results.prettify())
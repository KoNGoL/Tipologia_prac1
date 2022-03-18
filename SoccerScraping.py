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
        for team in teams_list:
            team_link = team.find('a')
            print(team_link)








URL = "https://fbref.com/es/comps/12/Estadisticas-de-La-Liga/"
base_url = 'https://fbref.com/'
soccer_scraping = SoccerScraping(URL, base_url)
soccer_scraping.find_teams()
#buscamos los equipos

#print(page.text)

#results = soup.find(id="ResultsContainer")

#print(results.prettify())
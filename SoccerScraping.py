__author__ = 'agr70'

import requests
from bs4 import BeautifulSoup
import pandas as pd


class SoccerScraping:


    def __init__(self, url, base_url):
        self.url = url
        self.data = pd.DataFrame()
        self.teams = []
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
        print("Obteniendo la lista de los equipos")
        for team in teams_list:
            team_link = team.find('a')
            team_link_str = str(team_link)

            string_ind_ini = team_link_str.index('">') + 2
            string_ind_end = team_link_str.index('a>') - 2
            team_clean = team_link_str[string_ind_ini:string_ind_end]

            teams_list_clean.append(team_clean)
            #print(team_clean)

            self.teams.append({'team': team_link.text, 'path': team_link.get('href')})

        print("Total equipos encontrados: {}".format(len(self.teams)))


    def find_team_players(self, team_name, team_url):
        print("Buscando jugadores del equipo {}".format(team_name))
        players = []
        team_request = requests.get(team_url, verify=False)
        team_html = BeautifulSoup(team_request.content, "html.parser")
        team_table = team_html.find(class_="table_container").find('tbody')
        team_players = team_table.find_all('tr')
        for player_row in team_players:
            player_name_cell = player_row.find('th').find('a')
            players.append({'name': player_name_cell.text, 'url': player_name_cell.get('href'), 'games_link': player_row.find('td', {'data-stat': 'matches'}).find('a').get('href')})

        print("Total jugadores encontrados: {}".format(len(players)))

        self.find_player_games_data(players[0])


    def find_player_games_data(self, player):
        print("Buscando info del jugador {}".format(player['name']))
        player_games_request = requests.get(self.base_url + player['games_link'], verify=False)
        player_games_html = BeautifulSoup(player_games_request.content, "html.parser")
        player_games_rows = player_games_html.find(id='matchlogs_all').find('tbody').find_all('tr')



URL = "https://fbref.com/es/comps/12/Estadisticas-de-La-Liga/"
base_url = 'https://fbref.com/'
soccer_scraping = SoccerScraping(URL, base_url)
soccer_scraping.find_teams()
soccer_scraping.find_team_players(soccer_scraping.teams[0]['team'], base_url + soccer_scraping.teams[0]['path'])

#buscamos los equipos

#print(page.text)

#results = soup.find(id="ResultsContainer")

#print(results.prettify())
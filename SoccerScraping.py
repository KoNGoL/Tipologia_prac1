__author__ = 'agr70'

import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

class SoccerScraping:


    def __init__(self, url, base_url):
        self.url = url
        self.data = pd.DataFrame()
        self.teams = []
        self.base_url = base_url

        #inicializamos el html
        page = requests.get(url, verify=False)
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.keys = None


    def find_teams(self):
        # obtenemos la grid de los equipos
        teams_grid = self.soup.find(id="stats_squads_standard_for").find('tbody')
        # obtenemos la lista de los equipos
        teams_list = teams_grid.find_all('tr')
        teams_list_clean = []
        teams_urls = []
        print("Obteniendo la lista de los equipos")
        for team in teams_list:
            team_link = team.find('a')
            #team_link_str = str(team_link)

            #string_ind_ini = team_link_str.index('">') + 2
            #string_ind_end = team_link_str.index('a>') - 2
            #team_clean = team_link_str[string_ind_ini:string_ind_end]

            #teams_list_clean.append(team_clean)
            
            #string_url_ini = team_link_str.index('href="') + 6
            #string_url_end = team_link_str.index('>') - 1
            #team_url = team_link_str[string_url_ini:string_url_end]
            #teams_urls.append(team_url)
            
            #teams_dict = dict(zip(teams_list_clean, teams_urls))
            #print(teams_dict)
            #print(team_clean)

            self.teams.append({'team_name': team_link.text, 'path': team_link.get('href')})

        print("Total equipos encontrados: {}".format(len(self.teams)))


    def scrap_data(self):
        for team in self.teams:
            self.find_team_players(team)

    def find_team_players(self, team):
        print("Buscando jugadores del equipo {}".format(team['team_name']))
        players = []
        team_request = requests.get(self.base_url + team['path'], verify=False)
        team_html = BeautifulSoup(team_request.content, "html.parser")
        team_table = team_html.find(class_="table_container").find('tbody')
        team_players = team_table.find_all('tr')
        # recorremos todos los jugadores del equipo
        for player_row in team_players:
            player_name_cell = player_row.find('th').find('a')
            players.append({'name': player_name_cell.text, 'url': player_name_cell.get('href'), 'games_link': player_row.find('td', {'data-stat': 'matches'}).find('a').get('href')})

        print("Total jugadores encontrados: {}".format(len(players)))
        team['players'] = players
        # recorremos todos los jugadores del equipo para extraer sus estadisticas
        for player in players:
            player['games'] = self.find_player_games_data(player)


    def find_player_games_data(self, player):
        print("Buscando info del jugador {}".format(player['name']))
        games_info = []
        player_games_request = requests.get(self.base_url + player['games_link'], verify=False)
        player_games_html = BeautifulSoup(player_games_request.content, "html.parser")
        # obtenemos las filas de los partidos
        player_games_rows = player_games_html.find(id='matchlogs_all').find('tbody').find_all('tr')
        print("Total partidos encontrados para el jugador {}: {}".format(player['name'], len(player_games_rows)))
        # recorremos los partidos para obtener las estadisticas
        for game in player_games_rows:
            game_info = {}
            # añadimos el primer campo al ser un th
            date_cell = game.find('th')
            game_info[date_cell.get('data-stat')] = date_cell.text

            # recorremos las diferentes celdas
            game_cells = game.find_all('td')
            for cell in game_cells :
                #print(cell.get('data-stat'))
                game_info[cell.get('data-stat')] = cell.text


            # guardmaos las keys para luego exportar a CSv
            if self.keys == None:
                self.keys = game_info.keys()

            # añadimos la info dle partido
            games_info.append(game_info)

        return games_info


    def export_csv(self):
        print("Exportando información.")
        # generamos la cabecera del csv
        csv = "'equipo';'jugador';"
        for key in self.keys:
             csv += "'{}';".format(key)
        csv += "\n"

        # guardamos los datos extraidos en el csv
        for team in self.teams:
            for player in team['players']:
                for game in player['games']:
                    csv += "'" + team['team_name'] + "';'" + player['name'] + "';"
                    for key in self.keys:
                        if key in game:
                            csv +="'" + game[key] + "';"
                        else:
                            csv +="'';"
                    csv += "\n"

        # guardamos el fichero
        f = open("/home/fundamentia/PycharmProjects/Tipologia_prac1/players_info.csv", "w")
        f.write(csv)
        f.close()


URL = "https://fbref.com/es/comps/12/Estadisticas-de-La-Liga/"
base_url = 'https://fbref.com/'
soccer_scraping = SoccerScraping(URL, base_url)
soccer_scraping.find_teams()
soccer_scraping.scrap_data()
soccer_scraping.export_csv()

#buscamos los equipos

#print(page.text)

#results = soup.find(id="ResultsContainer")

#print(results.prettify())


















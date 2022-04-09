__author__ = 'agr70'

import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

class SoccerScraping:


    def __init__(self, url, base_url):
        self.url = url
        self.data = pd.DataFrame()
        self.teams = []
        self.base_url = base_url

        #inicializamos el html
        self.soup = self.invokeUrl(url)
        self.keys = set()


    def find_teams(self):
        """
        Encuentra todos los equipos en la web

        Parameters: None
        """
        # obtenemos la grid de los equipos
        teams_grid = self.soup.find_all(class_="styled__ItemContainer-fyva03-1")
        # obtenemos la lista de los equipos
        print("Obteniendo la lista de los equipos")
        for team in teams_grid:
            team_link = team.find('a').get('href')
            team_name = team.find('h2').text
            self.teams.append({'team_name': team_name, 'path': team_link})

        print("Total equipos encontrados: {}".format(len(self.teams)))


    def scrap_data(self):
        """
        Inicia el Scrap de cada equipo encontrado

        Parameters: None
        """
        for team in self.teams:
            self.find_team_players(team)


    def find_team_players(self, team):
        """
        Encuentra todos los jugadores de un equipo y extrae sus datos

        Parameters:
        team: equipo a buscar

        """
        print("Buscando jugadores del equipo {}".format(team['team_name']))
        players = []
        team_html = self.invokeUrl(self.base_url + team['path'] + '/plantilla')
        team_players = team_html.find(class_='styled__SquadListContainer-sx1q1t-0').find_all(class_="styled__CellStyled-vl6wna-0")
        players_found = set()
        # recorremos todos los jugadores del equipo
        for player_cell in team_players:
            #comprobamos que no sea un entrenador o asistente
            if 'entrenador' in player_cell.text.lower():
                continue
            player_link = player_cell.find('a').get('href')
            player_name = player_cell.find('p').text
            if player_name in players_found:
                continue
            players_found.add(player_name)
            players.append({'name': player_name, 'url': player_link})

        print("Total jugadores encontrados: {}".format(len(players)))
        team['players'] = players
        # recorremos todos los jugadores del equipo para extraer sus estadisticas
        for player in players:
            player['stats'] = self.find_player_stats(player)


    def find_player_stats(self, player):
        """
        Extrae los datos de un jugador

        Parameters:
        player: juggador a extraer sus datos

        Retuns:
        Datos del jugador
        """
        print("Buscando info del jugador {}".format(player['name']))
        player_stats = {}
        player_html = self.invokeUrl(self.base_url + player['url'])
        time.sleep(30)
        #obtenemos las estadisticas del jugador
        player_stats_rows = player_html.find_all(class_='styled__StatsCol-sc-19ye3lp-4')
        for stat in player_stats_rows:
            stat_key = stat.find(class_='styled__StatsColLabel-sc-19ye3lp-7').find('p').text
            stat_value = stat.find(class_='styled__StatsColValue-sc-19ye3lp-8').find('p').text
            player_stats[stat_key] = stat_value
            self.keys.add(stat_key)

        return player_stats


    def export_csv(self):
        """
        Exporta los datos a un CSV

        Parameters: None

        """
        print("Exportando información.")
        # generamos la cabecera del csv
        csv = "'equipo';'jugador';"
        for key in self.keys:
             csv += "'{}';".format(key)
        csv += "\n"

        # guardamos los datos extraidos en el csv
        for team in self.teams:
            for player in team['players']:
                csv += "'" + team['team_name'] + "';'" + player['name'] + "';"
                for key in self.keys:
                    if 'stats' not in player :
                        csv +="'';"
                    elif key in player['stats']:
                        csv +="'" + player['stats'][key] + "';"
                    else:
                        csv +="'';"
                csv += "\n"

        # guardamos el fichero
        f = open("/home/fundamentia/PycharmProjects/Tipologia_prac1/players_info.csv", "w")
        f.write(csv)
        f.close()


    def invokeUrl(self, url):
        """
        Invoca una URl y general su html

        Parameters:
        url (string): url a la que invocar

        Return:
        (object) Html de la URL descargada
        """
        team_request = requests.get(url, verify=False)
        if team_request.status_code == 202:
            html = BeautifulSoup(team_request.content, "html.parser")
            time.sleep(30)
            return html
        else:
            # si da error, se esperan 30 seg y se reintata la llamada
            time.sleep(30)
            team_request = requests.get(url, verify=False)
            if team_request.status_code == 202:
                html = BeautifulSoup(team_request.content, "html.parser")
                time.sleep(30)
                return html
            else:
                print("ERROR AL INVOCAR LA URL: {}".format(url))
        return None



URL = "https://www.laliga.com/laliga-santander/clubes"
base_url = 'https://www.laliga.com/'
soccer_scraping = SoccerScraping(URL, base_url)
soccer_scraping.find_teams()
soccer_scraping.scrap_data()
soccer_scraping.export_csv()

#buscamos los equipos

#print(page.text)

#results = soup.find(id="ResultsContainer")

#print(results.prettify())


















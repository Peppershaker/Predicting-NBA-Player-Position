import requests
import re
import os

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from tqdm import tqdm

class espn_player_scraper():
    def _get_team_page_urls(self, teams_overview_url):
        a_style = "padding-left:0px;margin:0px;float:left;width:50px;text-decoration:none"

        teams_soup = BeautifulSoup(requests.get(teams_overview_url).content, 'html.parser')
        team_a_list = teams_soup.findAll('a', {'style':'padding-top:5px;padding-left:0px;'})

        team_urls_dict = dict()
        for a in team_a_list:
            team_url = "http://www.espn.com" + a['href']
            team_name = a.text
            team_urls_dict[team_name] = team_url

        return team_urls_dict

    def _get_players_form_team_soup(self, team_url):
        """
        Takes ESPN team url and returns a list of soup objects 
        each corresponding to a player on the team
        """
        response = requests.get(team_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        player_table_soup = soup.findAll('tr', attrs={"class":"Table2__tr Table2__tr--lg Table2__even"})

        return player_table_soup


    def _get_players_info(self, player_row_soup):
        """
        Takes soup object for the player of interest and returns relevant info in a list
        """
        player_info_str = player_row_soup.text

        # Get player name
        name_pattern = re.compile(r"[A-Za-z '.-]+")
        name_result = re.search(name_pattern, player_info_str)

        if name_result is not None:
            player_name = name_result.group(0)
        else:
            player_name = np.nan

        # Get player position
        position_pattern = re.compile(r"[A-Za-z '.-]+[0-9]+([A-Z]+)[0-9]+")
        position_result = re.search(position_pattern, player_info_str)
        
        if position_result is not None:
            player_position = position_result.group(1)
        else:
            player_position = np.nan

        # Get player ESPN id. This id is different than the NBA player id
        player_espn_url = player_row_soup.find('a')['href']
        player_id_result = re.search(re.compile('[0-9]{3,}'), player_espn_url)
        
        if player_id_result is not None:
            player_id = player_id_result.group(0)
        else:
            player_id = np.nan

        return [player_name, player_position, player_id, player_espn_url]
    
    def scrape_all_players(self, teams_overview_url):
        """
        Scrape ESPN for player information. Limited to only players active in
        2018-2019 season.

        Args:
            :teams_overview_url: ESPN page with all the teams in the league.
            (http://www.espn.com/nba/players)

        Returns:
            :A data frame containing all players, their espn id, position, and
            ESPN player profile page url
        """
        
        # Scrape all player info
        teams_overview_url = "http://www.espn.com/nba/players"
        team_url_dict = self._get_team_page_urls(teams_overview_url)
        player_scraping_result = []

        # Iterate through all teams to get players for each team
        for team_name, team_url in tqdm(team_url_dict.items()):
            team_soup = self._get_players_form_team_soup(team_url)

            for player_soup in team_soup:
                player_info = self._get_players_info(player_soup)
                player_scraping_result.append(player_info)

        players_df = pd.DataFrame(player_scraping_result, columns=['name', 'position',  "espn_player_id", 'url'])

        return players_df
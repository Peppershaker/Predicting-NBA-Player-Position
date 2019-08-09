import pytest
import pickle

from src.espn_scraper import espn_player_scraper

@pytest.fixture
def scraper():
    scraper = espn_player_scraper()
    return scraper


def test_get_team_page_urls(scraper):
    team_overview_url = "http://www.espn.com/nba/players" 
    team_url_dict = scraper._get_team_page_urls(team_overview_url)

    with open('tests/pickle/team_url_dict.pickle','rb') as f:
        team_url_dict_ground_truth = pickle.load(f)

    assert team_url_dict == team_url_dict_ground_truth

def test_get_player_info(scraper):
    team_url = 'https://www.espn.com/nba/team/roster/_/name/bos/boston-celtics'
    team_soup = scraper._get_players_form_team_soup(team_url)

    carsen_edwards_soup = team_soup[1]
    carsen_edwards_info = scraper._get_players_info(carsen_edwards_soup)

    assert carsen_edwards_info == ["Carsen Edwards", 
                                   "PG", 
                                   "4066407", 
                                   "http://www.espn.com/nba/player/_/id/4066407/carsen-edwards"] 
    
    

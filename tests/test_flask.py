import requests
import pandas as pd

from src.player_stat import get_player_stat


def test_api():
    player_ids_to_test = ['2544','1627783','202326','203081','1629014']
    
    player_labels = ['PG', 'PF', 'C', 'PG', 'SG']

    label_encoder_dict = dict([
        ("C",0),
        ("PG",1),
        ("SG",2),
        ("SF",3),
        ("PF",4)])
    
    player_labels_int = [label_encoder_dict[label] for label in player_labels]

    header = {'Content-Type': 'application/json', 
              'Accept': 'application/json'}

    request_url = "http://127.0.0.1:5000/predict"

    for player_id, player_label in zip(player_ids_to_test, player_labels_int):
        player_test_data = get_player_stat(player_id).to_json(orient='records')

        r = requests.post(request_url, data=player_test_data, headers=header)
        
        predicted_label = pd.read_json(r.content).values[0][0]

        print(player_id, predicted_label, player_label)
        assert predicted_label == int(player_label)

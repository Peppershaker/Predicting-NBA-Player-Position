import pandas as pd
from nba_py import player
import sys
sys.path.append('/Users/victor/Documents/code/nba_api')


class NoDataError(Exception):
    """Error indicating no data is returned by the API, this is usually caused by players not playing enough matches to generate the stats requested"""
    pass


def get_player_stat(player_id):
    """
    Takes player NBA ID and returns a data frame containing player performance
    data such as shooting, blocking, rebound etc...
    """
    # Extracting shooting and blocking columns
    player_shot_block_raw = player.PlayerShootingSplits(player_id).shot_areas()

    if player_shot_block_raw.shape[0] == 0:
        raise NoDataError("No data for {}".format(player_id))

    player_shot_and_block_by_area = player_shot_block_raw.T
    player_shot_and_block_by_area.columns = player_shot_and_block_by_area.loc['GROUP_VALUE']
    player_shot_and_block_by_area = player_shot_and_block_by_area.loc[[
        'FGA', 'BLKA'], "Restricted Area":"Above the Break 3"]

    player_shot_by_area = player_shot_and_block_by_area.loc[["FGA"], :]
    player_block_by_area = player_shot_and_block_by_area.loc[["BLKA"], :]

    # Use a dict to map old col name to new col name, using dict is required
    # because the API sometimes returns inconsistent column order and number
    # of cols
    shot_col_map = {"Restricted Area": 'shot_res',
                    "In The Paint (Non-RA)": 'shot_in_paint',
                    "Mid-Range": 'shot_mid_range',
                    'Left Corner 3': 'shot_lcorner_3',
                    'Right Corner 3': 'shot_rcorner_3',
                    'Above the Break 3': 'shot_above_3'}

    block_col_map = {"Restricted Area": 'block_res',
                     "In The Paint (Non-RA)": 'block_in_paint',
                     "Mid-Range": 'block_mid_range',
                     'Left Corner 3': 'block_lcorner_3',
                     'Right Corner 3': 'block_rcorner_3',
                     'Above the Break 3': 'block_above_3'}

    # Applying the column name map
    player_shot_by_area = player_shot_by_area.rename(columns=shot_col_map)
    player_block_by_area = player_block_by_area.rename(columns=block_col_map)

    # Total attempted shots and blocks
    total_shots = player_shot_by_area.loc['FGA', :].sum()
    total_blocks = player_block_by_area.loc['BLKA', :].sum()

    # Normalize all stats by total shots to get relative frequencies for each
    # player
    player_shot_by_area /= total_shots + 1e-5
    player_block_by_area /= total_blocks + 1e-5

    # Record total attempted shots and blocks
    player_shot_by_area['fga'] = total_shots
    player_block_by_area['blka'] = total_blocks

    # PlayerYearOverYearSplits is the end point we will be calling
    # to get player stats aside from shooting and blocking
    # Take the most recent 2 years, and then add them
    rebound_assist = player.PlayerYearOverYearSplits(
        player_id, per_mode="Per48").by_year().iloc[:2, :]

    cols_of_interest = ['OREB', 'DREB', 'AST', 'STL', "MIN"]

    rebound_assist = rebound_assist[cols_of_interest]
    rebound_assist.columns = [c.lower() for c in rebound_assist.columns]
    rebound_assist_summed = pd.DataFrame(rebound_assist.sum()).T

    # Finally, concatnate the dataframes together
    player_stat = pd.concat([player_shot_by_area.reset_index(drop=True),
                             player_block_by_area.reset_index(drop=True),
                             rebound_assist_summed.reset_index(drop=True)],
                            axis=1)
    player_stat = player_stat.rename({0: player_id})

    return player_stat

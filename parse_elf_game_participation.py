
from datetime import datetime
import json
import numpy as np

import pandas as pd
from tqdm import tqdm

from elf_utils import get_json_in_folder


def parse_elf_game_participation(save=False):
    json_file_list = get_json_in_folder()
    participation_df = pd.DataFrame()
    row_df = pd.DataFrame()

    # print(json_file_list)

    for json_file in tqdm(json_file_list):
        with open(json_file, 'r') as f:
            json_string = f.read()

        # print(f'\n{json_file}')
        json_data = json.loads(json_string)

        game_id = json_data['venue']['_attributes']['gameid']

        game_date = str(json_data['venue']['_attributes']['date'])
        game_date = datetime.strptime(game_date, '%m/%d/%Y')
        game_season = game_date.year

        home_id = json_data['venue']['_attributes']['homeid']
        home_name = json_data['venue']['_attributes']['homename']

        visitor_id = json_data['venue']['_attributes']['visid']
        visitor_name = json_data['venue']['_attributes']['visname']

        for i in json_data['visitor_players']:
            # print(i['_attributes']['name'])
            row_df = pd.DataFrame(
                {
                    'season': game_season,
                    'game_id': game_id,
                    'team_id': visitor_id,
                    'team_name': visitor_name,
                    'loc': 'A',
                    'opponent_id': home_id,
                    'opponent_name': home_name

                },
                index=[0]
            )
            row_df['player_uni'] = i['_attributes']['uni']
            row_df['player_name'] = i['_attributes']['name']
            row_df['player_short_name'] = i['_attributes']['shortname']
            row_df['player_check_name'] = i['_attributes']['checkname']
            row_df['player_GP'] = i['_attributes']['gp']

            try:
                row_df['player_GS'] = int(i['_attributes']['gs'])
            except:
                row_df['player_GS'] = 0

            try:
                row_df['player_pos'] = i['_attributes']['opos']
            except:
                try:
                    row_df['player_pos'] = i['_attributes']['dpos']
                except:
                    row_df['player_pos'] = None

            participation_df = pd.concat(
                [participation_df, row_df],
                ignore_index=True
            )
            del row_df

        for i in json_data['visitor_players']:
            row_df = pd.DataFrame(
                {
                    'season': game_season,
                    'game_id': game_id,
                    'opponent_id': home_id,
                    'opponent_name': home_name,
                    'loc': 'A',
                    'team_id': visitor_id,
                    'team_name': visitor_name
                },
                index=[0]
            )
            row_df['player_uni'] = i['_attributes']['uni']
            row_df['player_name'] = i['_attributes']['name']
            row_df['player_short_name'] = i['_attributes']['shortname']
            row_df['player_check_name'] = i['_attributes']['checkname']
            row_df['player_GP'] = i['_attributes']['gp']

            try:
                row_df['player_GS'] = int(i['_attributes']['gs'])
            except:
                row_df['player_GS'] = 0

            try:
                row_df['player_pos'] = i['_attributes']['opos']
            except:
                try:
                    row_df['player_pos'] = i['_attributes']['dpos']
                except:
                    row_df['player_pos'] = None

            participation_df = pd.concat(
                [participation_df, row_df],
                ignore_index=True
            )
            del row_df

    if save == True:
        seasons_arr = participation_df['season'].to_numpy()
        seasons_arr = np.unique(seasons_arr)

        for s in seasons_arr:
            season_df = participation_df.loc[participation_df['season'] == s]
            season_df.to_csv(
                f'player_info/participation_data/csv/{s}_elf_participation.csv',
                index=False
            )

            season_df.to_parquet(
                f'player_info/participation_data/parquet/{s}_elf_participation.parquet',
                index=False
            )

    # print(participation_df)
    return participation_df


if __name__ == "__main__":
    parse_elf_game_participation(True)

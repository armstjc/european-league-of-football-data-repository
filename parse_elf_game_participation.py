
import json
import logging
from datetime import datetime

import numpy as np
import pandas as pd
from tqdm import tqdm

from elf_utils import get_csv_in_folder, get_json_in_folder


def parse_elf_game_participation(season: int, save=False):
    """

    """
    now = datetime.now()
    filter_by_season = False

    if season == 0:
        pass
    elif season > now.year:
        raise ValueError(f'`season` cannot be greater than {now.year}.')
    elif season < 2021:
        raise ValueError('`season` cannot be less than 2021.')
    else:
        filter_by_season = True

    json_file_list = get_json_in_folder()
    participation_df = pd.DataFrame()
    row_df = pd.DataFrame()

    # print(json_file_list)

    for json_file in tqdm(json_file_list):
        with open(json_file, 'r') as f:
            json_string = f.read()

        # print(f'\n{json_file}')
        json_data = json.loads(json_string)

        try:
            check = json_data["status"]
        except Exception:
            check = 200

        try:
            check = json_data["statusCode"]
        except Exception as e:
            logging.info(
                "No `statusCode` present in this JSON file. " +
                f"Full exception `{e}`"
            )

        if check == 200:
            game_id = json_data['venue']['_attributes']['gameid']

            game_date = str(json_data['venue']['_attributes']['date'])
            if "." in game_date:
                game_date = datetime.strptime(
                    game_date, '%m.%d.%Y'
                )
            else:
                try:
                    game_date = datetime.strptime(
                        game_date, '%m/%d/%Y'
                    )
                except Exception:
                    game_date = datetime.strptime(
                        f"{game_date}/{season}", '%m/%d/%Y'
                    )
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

                if str(i['_attributes']['name']).lower() != 'team' \
                        and str(i['_attributes']['name']).lower() != 'tm':
                    row_df['player_uni'] = i['_attributes']['uni']
                    row_df['player_name'] = i['_attributes']['name']
                    row_df['player_short_name'] = i['_attributes']['shortname']
                    row_df['player_check_name'] = i['_attributes']['checkname']
                    row_df['player_GP'] = i['_attributes']['gp']

                    try:
                        row_df['player_GS'] = int(i['_attributes']['gs'])
                    except Exception as e:
                        logging.info(
                            "Could not find any evidence " +
                            "that this player started this game. " +
                            f"Full exception `{e}`"
                        )
                        row_df['player_GS'] = 0

                    try:
                        row_df['player_pos'] = i['_attributes']['opos']
                    except Exception:
                        try:
                            row_df['player_pos'] = i['_attributes']['dpos']
                        except Exception as e:
                            logging.info(
                                "Could not find a position for this player. " +
                                f"Full exception `{e}`"
                            )

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

                if str(i['_attributes']['name']).lower() != 'team' \
                        and str(i['_attributes']['name']).lower() != 'tm':

                    row_df['player_uni'] = i['_attributes']['uni']
                    row_df['player_name'] = i['_attributes']['name']
                    row_df['player_short_name'] = i['_attributes']['shortname']
                    row_df['player_check_name'] = i['_attributes']['checkname']
                    row_df['player_GP'] = i['_attributes']['gp']

                    try:
                        row_df['player_GS'] = int(i['_attributes']['gs'])
                    except Exception:
                        row_df['player_GS'] = 0

                    try:
                        row_df['player_pos'] = i['_attributes']['opos']
                    except Exception:
                        try:
                            row_df['player_pos'] = i['_attributes']['dpos']
                        except Exception:
                            row_df['player_pos'] = None

                    participation_df = pd.concat(
                        [participation_df, row_df],
                        ignore_index=True
                    )
                    del row_df

    # Roster Data (to map player IDs)
    roster_file_list = get_csv_in_folder('rosters/')
    all_rosters_df = pd.DataFrame()
    r_df = pd.DataFrame()

    for roster_file in roster_file_list:
        r_df = pd.read_csv(roster_file)
        all_rosters_df = pd.concat([all_rosters_df, r_df], ignore_index=True)
        del r_df

    all_rosters_df = all_rosters_df[[
        'season', 'player_id', 'old_player_id', 'team', 'player_short_name'
    ]]
    all_rosters_df = all_rosters_df.rename(columns={'team': 'team_name'})

    participation_df = pd.merge(
        participation_df,
        all_rosters_df,
        how='left',
        on=['season', 'team_name', 'player_short_name']
    )

    del all_rosters_df

    if filter_by_season is True:
        participation_df = participation_df.loc[
            participation_df['season'] == season
        ]

    if save is True:
        seasons_arr = participation_df['season'].to_numpy()
        seasons_arr = np.unique(seasons_arr)

        for s in seasons_arr:
            season_df = participation_df.loc[participation_df['season'] == s]
            season_df.to_csv(
                f'player_info/participation_data/{s}_elf_participation.csv',
                index=False
            )

            # season_df.to_parquet(
            #     f'player_info/participation_data/{s}_elf_participation.parquet',
            #     index=False
            # )

    # print(participation_df)
    return participation_df


if __name__ == "__main__":
    now = datetime.now()

    parse_elf_game_participation(now.year, True)

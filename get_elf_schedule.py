import json
import logging
import time
from datetime import datetime, timedelta
from urllib.request import urlopen

import numpy as np
import pandas as pd
# import requests
# from bs4 import BeautifulSoup
from tqdm import tqdm


def get_elf_schedule(season_filter=0, return_all_games=False, save=False):
    print('')
    schedule_url = "https://elf-app-89392.web.app/apiPublic/dump/gamedays?"
    games_url = "https://elf-app-89392.web.app/apiPublic/dump/games?"

    now = datetime.now()
    row_df = pd.DataFrame()
    sched_df = pd.DataFrame()
    game_info_df = pd.DataFrame()
    finished_df = pd.DataFrame()

    if return_all_games is True:
        logging.info('Retrieving every ELF game played and scheduled.')
    elif season_filter < 2021:
        raise ValueError(
            'The European League of Football (ELF) ' +
            'did not start play until 2021.'
        )
    elif season_filter > now.year:
        raise ValueError(
            'The input for `season_filter` cannot be greater ' +
            'than the current year.'
        )

    print('Getting the list of ELF games.')
    time.sleep(0.5)

    response = urlopen(schedule_url)
    json_string = response.read()
    # json_string = str(json_string).replace('\\"','"')
    json_data = json.loads(json_string)

    del json_string

    print('Parsing the list of ELF games.')
    for (key, value) in tqdm(json_data.items()):
        # print(key)
        # print(f"\n{value}\n")
        season = int(value['year'])
        week = int(value['gameDayNumber'])
        week_str = value['displayName']

        for game_id in value['gameIds']:
            row_df = pd.DataFrame(
                {
                    'season': season,
                    'week': week,
                    'week_str': week_str,
                    'game_id': game_id
                },
                index=[0]
            )
            sched_df = pd.concat([sched_df, row_df], ignore_index=True)

            del row_df

        del season, week, week_str

    print('Getting additional ELF game info.')

    response = urlopen(games_url)
    json_string = response.read()
    # json_string = str(json_string).replace('\\"','"')
    json_data = json.loads(json_string)

    del json_string

    print('Parsing the additional ELF game info.')

    for (key, value) in tqdm(json_data.items()):
        row_df = pd.DataFrame({'game_id': key}, index=[0])

        try:
            row_df['date'] = datetime.fromtimestamp(
                value['date']['_seconds']) - timedelta(hours=1)
        except Exception as e:
            logging.info(
                "Could not get a valid date for this game. " +
                f"Full exception `{e}`"
            )
            row_df['date'] = None
        row_df['is_cancelled'] = value['isCancelled']
        row_df['away_team_id'] = value['away']['teamId']
        row_df['away_team_slug'] = value['away']['slug']
        row_df['away_team_name'] = value['away']['name']

        row_df['home_team_id'] = value['home']['teamId']
        row_df['home_team_slug'] = value['home']['slug']
        row_df['home_team_name'] = value['home']['name']

        row_df['away_team_score'] = value['away']['score']
        row_df['home_team_score'] = value['home']['score']

        row_df['gamebook_url'] = value['gamebook']
        row_df['is_game_over'] = value['gameOver']
        row_df['is_game_tbd'] = value['isTbd']
        row_df['has_game_started'] = value['gameHasStarted']
        row_df['sports_metrics_game_id'] = value['statsCrewGameId']
        row_df['old_game_id'] = value['slug']

        game_info_df = pd.concat([game_info_df, row_df], ignore_index=True)

        del row_df

    finished_df = pd.merge(
        sched_df,
        game_info_df,
        left_on=['game_id'],
        right_on=['game_id'],
        how='left'
    )

    del sched_df, game_info_df

    if return_all_games is False:
        finished_df = finished_df.loc[finished_df['season'] == season_filter]

    if save is True:
        print('Saving off ELF schedule data.')
        season_arr = finished_df['season'].to_numpy()
        season_arr = np.unique(season_arr)
        for s in tqdm(season_arr):
            season_df = finished_df.loc[finished_df['season'] == s]
            season_df.to_csv(f'schedule/{s}_elf_schedule.csv', index=False)
            # season_df.to_parquet(f'schedule/{s}_elf_schedule.parquet',index=False)

        del season_arr

    return finished_df


if __name__ == "__main__":
    get_elf_schedule(return_all_games=True, save=True)

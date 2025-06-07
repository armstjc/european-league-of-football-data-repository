import json
import time
from urllib.request import urlopen

import numpy as np
import pandas as pd


def get_elf_standings(save=False):
    print('')
    url = "https://elf-app-89392.web.app/apiPublic/dump/standings?"

    row_df = pd.DataFrame()
    standings_df = pd.DataFrame()
    standings_df_arr = []
    time.sleep(0.5)

    response = urlopen(url)
    json_string = response.read()
    # json_string = str(json_string).replace('\\"','"')
    json_data = json.loads(json_string)

    del json_string

    for (key, value) in json_data.items():
        team_id = value['teamId']
        row_df = pd.DataFrame({'team_id': team_id}, index=[0])
        row_df['season'] = int(value['season'])

        row_df['conference_id'] = value['conferenceId']
        row_df['division_id'] = value['divisionId']
        row_df['rank'] = int(value['rank'])
        row_df['team_abv'] = str(value['shortname']).upper()
        row_df['team_name'] = value['name']

        row_df['overall_wins'] = int(value['wins'])
        row_df['overall_losses'] = int(value['losses'])
        row_df['overall_win_pct'] = row_df['overall_wins'] / \
            (row_df['overall_wins'] + row_df['overall_losses'])
        row_df['overall_win_pct'] = row_df['overall_win_pct'].round(3)

        row_df['points_for'] = int(value['pf'])
        row_df['points_against'] = int(value['pa'])
        row_df['point_diff'] = row_df['points_for'] - row_df['points_against']

        row_df['conference_wins'] = int(value['confW'])
        row_df['conference_losses'] = int(value['confL'])
        row_df['conference_win_pct'] = row_df['conference_wins'] / \
            (row_df['conference_wins'] + row_df['conference_losses'])
        row_df['conference_win_pct'] = row_df['conference_win_pct'].round(3)

        row_df['conference_points_for'] = int(value['confPf'])
        row_df['conference_points_against'] = int(value['confPa'])
        row_df['conference_point_diff'] = row_df['conference_points_for'] - \
            row_df['conference_points_against']

        home_w, home_l = str(value['home']).split('-')
        home_w = int(home_w)
        home_l = int(home_l)
        row_df['home_wins'] = home_w
        row_df['home_losses'] = home_l

        if (home_w + home_l) > 0:
            row_df['home_win_pct'] = home_w / (home_w + home_l)
        else:
            row_df['home_win_pct'] = None

        del home_w, home_l

        away_w, away_l = str(value['away']).split('-')
        away_w = int(away_w)
        away_l = int(away_l)
        row_df['away_wins'] = away_w
        row_df['away_losses'] = away_l

        if (away_w + away_l) > 0:
            row_df['away_win_pct'] = away_w / (away_w + away_l)
        else:
            row_df['away_win_pct'] = None

        del away_w, away_l

        neutral_w, neutral_l = str(value['neutral']).split('-')

        try:
            neutral_w = int(neutral_w)
            neutral_l = int(neutral_l)
        except Exception:
            neutral_w = 0
            neutral_l = 0

        row_df['neutral_wins'] = neutral_w
        row_df['neutral_losses'] = neutral_l

        if (neutral_w + neutral_l) > 0:
            row_df['neutral_win_pct'] = neutral_w / (neutral_w + neutral_l)
        else:
            row_df['neutral_win_pct'] = None

        del neutral_w, neutral_l

        try:
            row_df['streak'] = value['streak']
        except Exception:
            row_df['streak'] = None
        standings_df_arr.append(row_df)

        del row_df
    standings_df = pd.concat(standings_df_arr, ignore_index=True)

    standings_df = standings_df.sort_values(
        ['season', 'conference_id', 'division_id', 'rank'], ascending=True)

    if save is True:
        seasons_arr = standings_df['season'].to_numpy()
        seasons_arr = np.unique(seasons_arr)

        for i in seasons_arr:
            seasons_df = standings_df.loc[standings_df['season'] == i]
            seasons_df.to_csv(
                f'standings/{i}_elf_standings.csv', index=False)
            # seasons_df.to_parquet(
            #     f'standings/{i}_elf_standings.parquet', index=False)

    return standings_df


if __name__ == "__main__":
    get_elf_standings(True)

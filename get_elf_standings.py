from datetime import datetime
import json
import time
from urllib.request import urlopen
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_elf_standings(save=False):
    print('')
    url = "https://elf-app-89392.web.app/apiPublic/dump/standings?"

    row_df = pd.DataFrame()
    standings_df = pd.DataFrame()
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

        row_df['confrence_id'] = value['conferenceId']
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

        row_df['confrence_wins'] = int(value['confW'])
        row_df['confrence_losses'] = int(value['confL'])
        row_df['confrence_win_pct'] = row_df['confrence_wins'] / \
            (row_df['confrence_wins'] + row_df['confrence_losses'])
        row_df['confrence_win_pct'] = row_df['confrence_win_pct'].round(3)

        row_df['confrence_points_for'] = int(value['confPf'])
        row_df['confrence_points_against'] = int(value['confPa'])
        row_df['confrence_point_diff'] = row_df['confrence_points_for'] - \
            row_df['confrence_points_against']

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
        except:
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
        except:
            row_df['streak'] = None

        standings_df = pd.concat([standings_df, row_df], ignore_index=True)

        del row_df

    standings_df = standings_df.sort_values(
        ['season', 'confrence_id', 'division_id', 'rank'], ascending=True)

    if save == True:
        seasons_arr = standings_df['season'].to_numpy()
        seasons_arr = np.unique(seasons_arr)

        for i in seasons_arr:
            seasons_df = standings_df.loc[standings_df['season'] == i]
            seasons_df.to_csv(
                f'standings/{i}_elf_standings.csv', index=False)
            # seasons_df.to_parquet(
            #     f'standings/{i}_elf_standings.parquet', index=False)

    return standings_df


def dep_get_elf_standings(season: int, save=True):
    """
    DEPRECATED! Use `get_elf_schedule()` instead!!

    Retrives the current European League of Football (ELF) 
    schedule for a given ELF season.
    """
    raise DeprecationWarning(
        'Due to a sudden, unexpected redesign of the ELF website, this function no longer works as intended. Use `get_elf_standings()` instead.')

    now = datetime.now()
    row_df = pd.DataFrame()
    standings_df = pd.DataFrame()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    if season < 2021:
        raise ValueError(
            'The European League of Football (ELF) did not start play until 2021.')
    elif season > now.year:
        raise ValueError(
            'The input for `season` cannot be greater than the current year.')

    standings_url = "https://europeanleague.football/standings"

    response = requests.get(standings_url, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')

    standings = soup.find(
        'div', {'data-w-tab': f'{season}'})

    confrences = standings.find_all('div', {'class': 'content-card-white'})
    # print(confrences)
    if season == 2021:
        for i in tqdm(confrences):
            conf = i.find('h3').text
            fixed_part = i.find('div', {'class': 'fixed-part'}).find_all(
                'div', {'class': 'w-dyn-item', 'role': 'listitem'})
            flex_part = i.find('div', {'class': 'flex-part'}).find_all(
                'div', {'class': 'w-dyn-item', 'role': 'listitem'})
            # print(f'\n\n\n{fixed_part}\n\n{flex_part}\n\n\n')
            conf_rk = 0
            for j in range(0, len(fixed_part)):
                tm_name = fixed_part[j]
                tm_record = flex_part[j].find_all(
                    'div', {'class': 'table-text'})

                conf_rk += 1
                # print(tm_record)

                row_df = pd.DataFrame(
                    {'season': season, 'confrence': conf, 'confrence_rank': conf_rk}, index=[0])
                row_df['team_name'] = tm_name.find(
                    'div', {'class': 'table-text is-team-name'}).text
                row_df['team_logo_url'] = tm_name.find(
                    'img', {'class': 'standings-logo'}).get('src')

                ovr_record = tm_record[0]
                ovr_record = ovr_record.text
                ovr_wins, ovr_losses = ovr_record.split('-')

                row_df['overall_record'] = ovr_record
                row_df['overall_wins'] = int(ovr_wins)
                row_df['overall_losses'] = int(ovr_losses)

                del ovr_record, ovr_wins, ovr_losses

                points_for = int(tm_record[2].text)
                points_against = int(tm_record[3].text)
                row_df['overall_win_pct'] = row_df['overall_wins'] / \
                    (row_df['overall_wins'] + row_df['overall_losses'])
                row_df['points_for'] = int(points_for)
                row_df['points_against'] = int(points_against)

                del points_for, points_against

                conf_record = tm_record[4].text
                conf_wins, conf_losses = conf_record.split('-')
                row_df['confrence_record'] = conf_record
                row_df['confrence_wins'] = int(conf_wins)
                row_df['confrence_losses'] = int(conf_losses)

                del conf_record, conf_wins, conf_losses

                row_df['confrence_win_pct'] = row_df['confrence_wins'] / \
                    (row_df['confrence_wins'] + row_df['confrence_losses'])
                conf_pf = int(tm_record[6].text)
                conf_pa = int(tm_record[7].text)

                row_df['confrence_points_for'] = conf_pf
                row_df['confrence_points_against'] = conf_pa

                del conf_pa, conf_pf

                home_record = tm_record[8].text
                home_wins, home_losses = home_record.split('-')
                home_wins = int(home_wins)
                home_losses = int(home_losses)
                row_df['home_record'] = home_record
                row_df['home_wins'] = home_wins
                row_df['home_losses'] = home_losses
                row_df['home_win_pct'] = home_wins / (home_wins + home_losses)

                del home_record, home_wins, home_losses

                away_record = tm_record[9].text
                away_wins, away_losses = away_record.split('-')
                away_wins = int(away_wins)
                away_losses = int(away_losses)
                row_df['away_record'] = away_record
                row_df['away_wins'] = away_wins
                row_df['away_losses'] = away_losses
                row_df['away_win_pct'] = away_wins / (away_wins + away_losses)

                del away_record, away_wins, away_losses

                neutral_record = tm_record[10].text
                neutral_wins, neutral_losses = neutral_record.split('-')
                neutral_wins = int(neutral_wins)
                neutral_losses = int(neutral_wins)
                row_df['neutral_record'] = neutral_record
                row_df['neutral_wins'] = neutral_wins
                row_df['neutral_losses'] = neutral_losses
                if (neutral_wins + neutral_losses) > 0:
                    row_df['neutral_win_pct'] = neutral_wins / \
                        (neutral_wins + neutral_losses)
                else:
                    row_df['neutral_win_pct'] = None
                del neutral_record, neutral_wins, neutral_losses

                streak = tm_record[11].text
                row_df['streak'] = streak

                del streak

                standings_df = pd.concat(
                    [standings_df, row_df], ignore_index=True)
    else:
        for i in tqdm(confrences):
            conf = i.find('h3').text
            fixed_part = i.find('div', {'class': 'fixed-part'}).find_all(
                'div', {'class': 'w-dyn-item', 'role': 'listitem'})
            flex_part = i.find('div', {'class': 'flex-part'}).find_all(
                'div', {'class': 'w-dyn-item', 'role': 'listitem'})
            # print(f'\n\n\n{fixed_part}\n\n{flex_part}\n\n\n')
            conf_rk = 0
            for j in range(0, len(fixed_part)):
                tm_name = fixed_part[j]
                tm_record = flex_part[j].find_all(
                    'div', {'class': 'table-text'})

                conf_rk += 1

                row_df = pd.DataFrame(
                    {'season': season, 'confrence': conf, 'confrence_rank': conf_rk}, index=[0])
                row_df['team_name'] = tm_name.find(
                    'div', {'class': 'table-text is-team-name'}).text
                row_df['team_logo_url'] = tm_name.find(
                    'img', {'class': 'standings-logo'}).get('src')

                ovr_wins = tm_record[0].text
                ovr_losses = tm_record[1].text
                ovr_record = f"{ovr_wins}-{ovr_losses}"

                row_df['overall_record'] = ovr_record
                row_df['overall_wins'] = int(ovr_wins)
                row_df['overall_losses'] = int(ovr_losses)

                del ovr_record, ovr_wins, ovr_losses

                points_for = int(tm_record[3].text)
                points_against = int(tm_record[4].text)
                row_df['overall_win_pct'] = row_df['overall_wins'] / \
                    (row_df['overall_wins'] + row_df['overall_losses'])
                row_df['points_for'] = int(points_for)
                row_df['points_against'] = int(points_against)

                del points_for, points_against

                conf_record = tm_record[5].text
                conf_wins, conf_losses = conf_record.split('-')
                row_df['confrence_record'] = conf_record
                row_df['confrence_wins'] = int(conf_wins)
                row_df['confrence_losses'] = int(conf_losses)

                del conf_record, conf_wins, conf_losses

                row_df['confrence_win_pct'] = row_df['confrence_wins'] / \
                    (row_df['confrence_wins'] + row_df['confrence_losses'])
                conf_pf = int(tm_record[7].text)
                conf_pa = int(tm_record[8].text)

                row_df['confrence_points_for'] = conf_pf
                row_df['confrence_points_against'] = conf_pa

                del conf_pa, conf_pf

                home_record = tm_record[9].text
                home_wins, home_losses = home_record.split('-')
                home_wins = int(home_wins)
                home_losses = int(home_losses)
                row_df['home_record'] = home_record
                row_df['home_wins'] = home_wins
                row_df['home_losses'] = home_losses
                row_df['home_win_pct'] = home_wins / (home_wins + home_losses)

                del home_record, home_wins, home_losses

                away_record = tm_record[10].text
                away_wins, away_losses = away_record.split('-')
                away_wins = int(away_wins)
                away_losses = int(away_losses)
                row_df['away_record'] = away_record
                row_df['away_wins'] = away_wins
                row_df['away_losses'] = away_losses
                row_df['away_win_pct'] = away_wins / (away_wins + away_losses)

                del away_record, away_wins, away_losses

                # neutral_record = tm_record[10].text
                # neutral_wins, neutral_losses = neutral_record.split('-')
                # neutral_wins = int(neutral_wins)
                # neutral_losses = int(neutral_wins)
                # row_df['neutral_record'] = neutral_record
                # row_df['neutral_wins'] = neutral_wins
                # row_df['neutral_losses'] = neutral_losses
                # if (neutral_wins + neutral_losses) > 0:
                #     row_df['neutral_win_pct'] = neutral_wins / \
                #         (neutral_wins + neutral_losses)
                # else:
                #     row_df['neutral_win_pct'] = None
                # del neutral_record, neutral_wins, neutral_losses

                streak = tm_record[11].text
                row_df['streak'] = streak

                del streak

                standings_df = pd.concat(
                    [standings_df, row_df], ignore_index=True)

    if save == True:
        standings_df.to_csv(
            f"standings/csv/{season}_elf_standings.csv", index=False)
        standings_df.to_parquet(
            f"standings/parquet/{season}_elf_standings.parquet", index=False)

    return standings_df


if __name__ == "__main__":
    get_elf_standings(True)

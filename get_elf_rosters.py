import glob
import json
import logging
import os
import time
from datetime import datetime
from urllib.request import urlopen

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from elf_utils import parse_position_names


def get_elf_rosters(save=False, season=0):
    now = datetime.now()
    rosters_df = pd.DataFrame()
    rosters_df_arr = []
    row_df = pd.DataFrame()
    season = now.year
    players_url = "https://elf-app-89392.web.app/apiPublic/dump/players?"

    # filter_out_seasons = False

    # if season >= 2021 and season <= now.year:
    #     filter_out_seasons = True

    response = urlopen(players_url)
    json_string = response.read()
    json_data = json.loads(json_string)

    del json_string

    for (key, value) in tqdm(json_data.items()):
        row_df = pd.DataFrame({'season': season, 'player_id': key}, index=[0])
        row_df['old_player_id'] = None
        row_df['team_abv'] = str(value['teamshort']).upper()
        row_df['team'] = None

        row_df['player_number'] = value['uni']

        row_df['player_first_name'] = value['firstname']
        row_df['player_last_name'] = value['lastname']
        row_df['player_short_name'] = value['cbsname']

        sec_pos = value['secpos']
        if sec_pos is None:

            row_df['player_position'] = parse_position_names(value['pos'])
        else:
            primary_position = parse_position_names(value['pos'])
            secondary_position = parse_position_names(value['secpos'])
            row_df['player_position'] = f"{
                primary_position}/{secondary_position}"

        try:
            row_df['player_height_m'] = int(value['height']) / 100
        except Exception as e:
            logging.info(
                f"Could not get player height in meters. Full exception `{e}`"
            )
            row_df['player_height_m'] = None

        row_df.loc[row_df['player_height_m'] > 0,
                   'player_height_in'] = row_df['player_height_m'] / 0.0254

        try:
            row_df['player_height_in'] = row_df['player_height_in'].round(2)
        except Exception as e:
            logging.info(
                f"Could not get player height in inches. Full exception `{e}`"
            )
            row_df['player_height_in'] = None

        try:
            row_df['player_weight_kg'] = int(value['weight'])
        except Exception as e:
            logging.info(
                f"Could not get player weight in KG. Full exception `{e}`"
            )
            row_df['player_weight_kg'] = None

        row_df.loc[
            row_df['player_weight_kg'] > 0,
            'player_weight_lbs'
        ] = row_df['player_weight_kg'] / 0.45359237

        try:
            row_df['player_weight_lbs'] = row_df['player_weight_lbs'].round(2)
        except Exception as e:
            logging.info(
                f"Could not get player weight in pounds. Full exception `{e}`"
            )
            row_df['player_weight_lbs'] = None

        row_df['birth_place'] = value['birthplace']
        row_df['birth_nation'] = value['nationbinding']
        row_df['primary_nation'] = value['nationone']
        row_df['secondary_nation'] = value['nationtwo']

        row_df['birthdate'] = value['birthdate']
        row_df['previous_team'] = value['previousteam']
        row_df['is_previous_contract'] = value['previouscontract']
        row_df['all_star'] = value['allstar']
        row_df['updated'] = value['updated']

        try:
            row_df['awards'] = value['awards']
        except Exception as e:
            logging.info(
                "Could not find any awards for this player. " +
                f"Full exception `{e}`"
            )
            row_df['awards'] = None

        row_df['player_headshot_url'] = value['avatar']
        rosters_df_arr.append(row_df)
        del row_df

    rosters_df = pd.concat(rosters_df_arr, ignore_index=True)

    if save is True:
        seasons_arr = rosters_df['season'].to_numpy()
        team_abv_arr = rosters_df['team_abv'].to_numpy()

        seasons_arr = np.unique(seasons_arr)
        team_abv_arr = np.unique(team_abv_arr)

        for s in seasons_arr:

            for t in team_abv_arr:
                team_df = rosters_df.loc[(rosters_df['season'] == s) & (
                    rosters_df['team_abv'] == t)]
                team_df.to_csv(f'rosters/raw/{s}_{t}.csv', index=False)

    return rosters_df


def get_old_elf_rosters(save=False, season=0):
    now = datetime.now()

    rosters_df = pd.DataFrame()
    rosters_df_arr = []
    row_df = pd.DataFrame()

    filter_out_seasons = False
    hit_wall = False

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) " +
        "Chrome/83.0.4103.97 Safari/537.36"
    }

    if season >= 2021 and season <= now.year:
        filter_out_seasons = True

    retries = 0
    page_num = 0
    running_count = 0

    while hit_wall is False:
        page_num += 1
        players_url = "https://europeanleague.football/league/players" +\
            f"?7e78f181_page={page_num}"
        time.sleep(1)

        response = requests.get(players_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        # print(response.encoding)
        if response.status_code == 200:
            soup = BeautifulSoup(
                response.text, features='lxml')
            # soup = soup.html.encode('utf-8')
            time.sleep(1)
            player_cards = soup.find_all('div', {'class': 'player-card'})
            player_count = len(player_cards)
            running_count = player_count + running_count

            for i in player_cards:  # tqdm(player_cards):
                player_id = str(i.find('a').get('href')).replace(
                    'player', '').replace('/', '')
                player_first_name = i.find(
                    'h3', {'fs-cmsfilter-field': 'first-name'}).text
                player_last_name = i.find(
                    'h3', {'fs-cmsfilter-field': 'last-name'}).text

                # print(f"\n{player_first_name} {player_last_name}")
                player_info = i.find('div', {'class': 'pc-info-part'})

                player_number = player_info.find(
                    'div', {'fs-cmsfilter-field': 'player-number'}).text

                player_position = player_info.find(
                    'div', {'fs-cmsfilter-field': 'pos'}).text
                try:
                    player_height_m = float(
                        str(
                            player_info.find(
                                'div', {'fs-cmsfilter-field': 'height'}
                            ).text
                        ).replace(',', '.')
                    )
                except Exception as e:
                    logging.info(
                        "Could not convert the player's height in meters " +
                        f"to a float. Full exception `{e}`"
                    )
                    player_height_m = None

                if player_height_m is not None:
                    player_height_in = round((player_height_m / 0.0254), 2)
                else:
                    player_height_in = None

                try:
                    player_weight_kg = int(player_info.find(
                        'div', {'fs-cmsfilter-field': 'weight'}).text)
                except Exception as e:
                    logging.info(
                        "Could not convert the player's weight in KG " +
                        f"to a float. Full exception `{e}`"
                    )
                    player_weight_kg = None

                if player_weight_kg is not None:
                    player_weight_lbs = round(
                        (player_weight_kg / 0.45359237), 2)
                else:
                    player_weight_lbs = None

                del player_info

                player_seasons = i.find_all(
                    'div', {'class': 'multi-item-line-wrapper'})

                for j in range(2, len(player_seasons)):
                    ps = player_seasons[j]

                    row_df = pd.DataFrame(
                        {
                            'player_id': player_id,
                            'player_number': player_number,
                            'player_first_name': player_first_name,
                            'player_last_name': player_last_name,
                            'player_position': player_position,
                            'player_height_m': player_height_m,
                            'player_height_in': player_height_in,
                            'player_weight_kg': player_weight_kg,
                            'player_weight_lbs': player_weight_lbs
                        },
                        index=[0]
                    )

                    player_season = int(
                        str(
                            ps.find_all(
                                'div',
                                {'class': 'pc-pre-heading is--multi-item'}
                            )[0].text
                        ).replace(' Team:', '')
                    )
                    player_team = ps.find_all(
                        'div', {'class': 'pc-pre-heading is--multi-item'}
                    )[1].text

                    if player_team == "-":
                        pass
                    else:
                        row_df['season'] = player_season
                        row_df['team'] = player_team
                        # rosters_df = pd.concat(
                        #     [rosters_df, row_df], ignore_index=True)

                    rosters_df_arr.append(row_df)
                    del row_df

            logging.info(
                f"{player_count} ELF players loaded in, " +
                f"{running_count} ELF players currently parsed."
            )

            if player_count < 50:
                logging.info('Finished parsing through the ELF players list.')
                hit_wall = True

            elif player_count == 0:
                logging.info('No further ELF players were found.')
                hit_wall = True

        elif retries < 5:
            logging.warning(
                "Couldn't load in player cards, attempting to reconnect. " +
                f"(Previous retries: {retries})")
            retries += 1

        elif retries == 5:
            logging.warning(
                "Aborting download/parsing of ELF player rosters. " +
                "Maximum retries reached."
            )
        else:
            hit_wall = True

    rosters_df = pd.concat(rosters_df_arr, ignore_index=True)
    if filter_out_seasons is True:
        team_df = rosters_df.loc[(rosters_df['season'] == season)]

    rosters_df = rosters_df.sort_values(
        by=['season', 'team', 'player_number', 'player_id'])

    if save is True:

        seasons_arr = rosters_df['season'].to_numpy()
        seasons_arr = np.unique(seasons_arr)

        for s in seasons_arr:
            teams_arr = rosters_df['team'].to_numpy()
            teams_arr = np.unique(teams_arr)

            for t in teams_arr:
                team_df = rosters_df.loc[(rosters_df['season'] == s) & (
                    rosters_df['team'] == t)]

                team_df.to_csv(f'rosters/raw/{s}_{t}.csv', index=False)

        # rosters_df.to_csv('rosters/csv/elf_rosters.csv', index=False)
    return rosters_df


def get_elf_player_ids(save=False):
    rosters_df = pd.DataFrame()
    rosters_df_arr = []
    row_df = pd.DataFrame()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) " +
        "Chrome/83.0.4103.97 Safari/537.36"
    }

    hit_wall = False
    retries = 0
    page_num = 0
    running_count = 0
    while hit_wall is False:
        page_num += 1
        players_url = "https://europeanleague.football/league/players" +\
            f"?7e78f181_page={page_num}"
        time.sleep(1)

        response = requests.get(players_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        # print(response.encoding)
        if response.status_code == 200:
            soup = BeautifulSoup(
                response.text, features='lxml')
            # soup = soup.html.encode('utf-8')
            time.sleep(1)
            player_cards = soup.find_all('div', {'class': 'player-card'})
            player_count = len(player_cards)
            running_count = player_count + running_count

            for i in player_cards:  # tqdm(player_cards):
                player_id = str(i.find('a').get('href')).replace(
                    'player', '').replace('/', '')
                player_first_name = i.find(
                    'h3', {'fs-cmsfilter-field': 'first-name'}).text
                player_last_name = i.find(
                    'h3', {'fs-cmsfilter-field': 'last-name'}).text

                # print(f"\n{player_first_name} {player_last_name}")
                player_info = i.find('div', {'class': 'pc-info-part'})

                player_number = player_info.find(
                    'div', {'fs-cmsfilter-field': 'player-number'}).text

                player_position = player_info.find(
                    'div', {'fs-cmsfilter-field': 'pos'}).text
                try:
                    player_height_m = float(
                        str(
                            player_info.find(
                                'div', {'fs-cmsfilter-field': 'height'}
                            ).text
                        ).replace(',', '.')
                    )
                except Exception as e:
                    logging.info(
                        "Could not convert player height " +
                        "in meters into a float. " +
                        f"Full exception `{e}`"
                    )
                    player_height_m = None

                if player_height_m is not None:
                    player_height_in = round((player_height_m / 0.0254), 2)
                else:
                    player_height_in = None

                try:
                    player_weight_kg = int(player_info.find(
                        'div', {'fs-cmsfilter-field': 'weight'}).text)
                except Exception as e:
                    logging.info(
                        "Could not convert player weight " +
                        "in KG into a float. " +
                        f"Full exception `{e}`"
                    )
                    player_weight_kg = None

                if player_weight_kg is not None:
                    player_weight_lbs = round(
                        (player_weight_kg / 0.45359237), 2)
                else:
                    player_weight_lbs = None

                del player_info

                # player_seasons = i.find_all(
                #     'div', {'class': 'multi-item-line-wrapper'})

                row_df = pd.DataFrame(
                    {
                        'player_id': player_id,
                        'player_number': player_number,
                        'player_first_name': player_first_name,
                        'player_last_name': player_last_name,
                        'player_position': player_position,
                        'player_height_m': player_height_m,
                        'player_height_in': player_height_in,
                        'player_weight_kg': player_weight_kg,
                        'player_weight_lbs': player_weight_lbs
                    },
                    index=[0]
                )
                rosters_df_arr.append(row_df)

            logging.info(
                f"{player_count} ELF players loaded in, " +
                f"{running_count} ELF players currently parsed."
            )

            if player_count < 50:
                logging.info('Finished parsing through the ELF players list.')
                hit_wall = True

            elif player_count == 0:
                logging.info('No further ELF players were found.')
                hit_wall = True

        elif retries < 5:
            logging.warning(
                "Couldn't load in player cards, attempting to reconnect. " +
                f"(Previous retries: {retries})"
            )
            retries += 1

        elif retries == 5:
            logging.warning(
                "Aborting download/parsing of ELF player rosters. " +
                "Maximum retries reached."
            )
        else:
            hit_wall = True
    rosters_df = pd.concat(rosters_df_arr, ignore_index=True)
    rosters_df = rosters_df.sort_values(
        by=['player_id'])

    if save is True:
        rosters_df.to_csv('player_info/elf_players.csv', index=False)

    return rosters_df


def generate_player_hist_file():
    now = datetime.now()
    rosters_df = pd.DataFrame()
    rosters_df_arr = []
    row_df = pd.DataFrame()

    players_url = "https://elf-app-89392.web.app/apiPublic/dump/players?"

    # filter_out_seasons = False

    response = urlopen(players_url)
    json_string = response.read()
    # json_string = str(json_string).replace('\\"','"')
    json_data = json.loads(json_string)

    del json_string

    for (key, value) in tqdm(json_data.items()):
        player_id = key

        first_name = value['firstname']
        last_name = value['lastname']
        birthday = value['birthdate']

        for i in value['teamhist']:
            if i['from'] is None:
                pass
            else:
                season = int(
                    str(
                        i['from']
                    ).replace(
                        '-01', ''
                    ).replace(
                        '-04', ''
                    ).replace(
                        '-07', ''
                    ).replace(
                        '-09', ''
                    ).replace(
                        '-11', ''
                    )
                )
                team = i['team']

                row_df = pd.DataFrame(
                    {
                        'season': season,
                        'team': team,
                        'player_id': player_id,
                        'player_first_name': first_name,
                        'player_last_name': last_name,
                        'birthday': birthday
                    },
                    index=[0]
                )
                rosters_df_arr.append(row_df)

                del row_df
    rosters_df = pd.concat(rosters_df_arr, ignore_index=True)
    rosters_df["last_updated"] = now.isoformat()
    rosters_df.to_csv('rosters/player_history/player_history.csv', index=False)
    print(rosters_df)


def generate_elf_roster_files(save=False):
    team_df = pd.DataFrame()
    rosters_df = pd.DataFrame()
    team_info_df = pd.read_csv('teams/elf_teams.csv')
    player_hist_df = pd.read_csv('rosters/player_history/player_history.csv')

    player_hist_df = player_hist_df[[
        'season', 'team', 'player_id', 'player_first_name', 'player_last_name'
    ]]

    filepath = os.path.abspath("rosters/raw")
    file_list = glob.iglob(filepath+"/*csv")
    file_list = list(file_list)
    file_list.sort(reverse=True)

    # print(file_list)

    for file in tqdm(file_list):
        team_df = pd.read_csv(file)
        rosters_df = pd.concat([rosters_df, team_df], ignore_index=True)

    old_rosters_df = rosters_df.loc[rosters_df['season'] <= 2022]
    new_rosters_df = rosters_df.loc[rosters_df['season'] >= 2023]
    # print(old_rosters_df)
    # print(new_rosters_df)

    del rosters_df
    old_rosters_df = old_rosters_df.drop(columns=['player_id'])

    team_name_abv_dict = dict(
        zip(team_info_df['team_name'], team_info_df['team_abv']))
    old_rosters_df['team_abv'] = old_rosters_df['team'].map(team_name_abv_dict)

    old_rosters_df['player_short_name'] = old_rosters_df[[
        'player_first_name', 'player_last_name'
    ]].apply(lambda x: f'{x[0][0]}. {x[1]}', axis=1)

    old_rosters_df = pd.merge(
        old_rosters_df,
        player_hist_df,
        how='left',
        on=['season', 'team', 'player_first_name', 'player_last_name']
    )

    del team_name_abv_dict, player_hist_df

    team_abv_name_dict = dict(
        zip(team_info_df['team_abv'], team_info_df['team_name'])
    )
    new_rosters_df['team'] = new_rosters_df['team_abv'].map(team_abv_name_dict)
    del team_abv_name_dict

    rosters_df = pd.concat([new_rosters_df, old_rosters_df], ignore_index=True)

    if save is True:
        seasons_arr = rosters_df['season'].to_numpy()
        seasons_arr = np.unique(seasons_arr)

        for i in seasons_arr:
            season_df = rosters_df.loc[rosters_df['season'] == i]
            season_df.to_csv(f'rosters/{i}_elf_rosters.csv', index=False)
            # season_df.to_parquet(
            #     f'rosters/{i}_elf_rosters.parquet', index=False)

    return rosters_df


if __name__ == "__main__":
    get_elf_rosters(True)
    generate_player_hist_file()
    generate_elf_roster_files(True)

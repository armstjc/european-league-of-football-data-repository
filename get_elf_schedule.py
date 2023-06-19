from datetime import datetime, timedelta
import json
import time
import numpy as np
import pandas as pd
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_elf_schedule(season_filter= 0, return_all_games=False, save=False):
    print('')
    schedule_url = "https://elf-app-89392.web.app/apiPublic/dump/gamedays?"
    games_url = "https://elf-app-89392.web.app/apiPublic/dump/games?"

    now = datetime.now()
    row_df = pd.DataFrame()
    sched_df = pd.DataFrame()
    game_info_df = pd.DataFrame()
    finished_df = pd.DataFrame()

    if return_all_games == True:
        print('Retriving every ELF game played and scheduled.')
    elif season_filter < 2021:
        raise ValueError(
            'The European League of Football (ELF) did not start play until 2021.')
    elif season_filter > now.year:
        raise ValueError(
            'The input for `season_filter` cannot be greater than the current year.')
    
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
            row_df = pd.DataFrame({'season':season,'week':week,'week_str':week_str,'game_id':game_id},index=[0])
            sched_df = pd.concat([sched_df,row_df],ignore_index=True)
            
            del row_df

        del season,week,week_str

    print('Getting additional ELF game info.')


    response = urlopen(games_url)
    json_string = response.read()
    # json_string = str(json_string).replace('\\"','"')
    json_data = json.loads(json_string)

    del json_string

    print('Parsing the additional ELF game info.')

    for (key,value) in tqdm(json_data.items()):
        row_df = pd.DataFrame({'game_id':key},index=[0])
        
        try:
            row_df['date'] = datetime.fromtimestamp(value['date']['_seconds']) - timedelta(hours=1)
        except:
            row_df['date'] = None

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
        row_df['stats_crew_game_id'] = value['statsCrewGameId']
        row_df['old_game_id'] = value['slug']

        game_info_df = pd.concat([game_info_df,row_df],ignore_index=True)
    
        del row_df

    finished_df = pd.merge(sched_df,game_info_df,left_on=['game_id'],right_on=['game_id'],how='left')

    del sched_df, game_info_df

    if return_all_games == False:
        finished_df = finished_df.loc[finished_df['season'] == season_filter]
    
    if save == True:
        print('Saving off ELF schedule data.')
        season_arr = finished_df['season'].to_numpy()
        season_arr = np.unique(season_arr)
        for s in tqdm(season_arr):
            season_df = finished_df.loc[finished_df['season']== s]
            season_df.to_csv(f'schedule/csv/{s}_elf_schedule.csv',index=False)
            season_df.to_parquet(f'schedule/parquet/{s}_elf_schedule.parquet',index=False)

        del season_arr

    return finished_df

def dep_get_elf_schedule(season: int, week=0, save=False):
    """
    DEPRECATED! Use `get_elf_schedule()` instead!!

    Retrives the current European League of Football (ELF) 
    schedule for a given ELF season.
    """
    raise DeprecationWarning('Due to a sudden, unexpected redesign of the ELF website, this function no longer works as intended. Use `get_elf_schedule()` instead.')
    now = datetime.now()
    row_df = pd.DataFrame()
    sched_df = pd.DataFrame()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    if season < 2021:
        raise ValueError(
            'The European League of Football (ELF) did not start play until 2021.')
    elif season > now.year:
        raise ValueError(
            'The input for `season` cannot be greater than the current year.')

    if week < 0:
        raise ValueError('`week` cannot be less than 0.')
    elif week > 14:
        raise ValueError(
            '`week` cannot be greater than 14 at this time.')

    normal_url = f"https://europeanleague.football/game-center/schedule?filters=eyJ3ZWVrcyI6WzFdLCJ5ZWFycyI6WzIwMjNdfQ=="
    time.sleep(0.5)

    response = requests.get(normal_url, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')

    games_list = soup.find('div', {'class': 'cms-filter-content'})

    games = games_list.find_all(
        'div', {"role": "listitem", "class": "w-dyn-item"})

    # with open('test.html', 'w+', encoding='latin') as f:
    #     f.write(str(games))

    del games_list
    for j in tqdm(games):
        game_season = int(
            j.find('div', {'fs-cmsfilter-field': 'season'}).text)

        if game_season == season:
            row_df = pd.DataFrame({'season': game_season}, index=[0])
            row_df['week'] = j.find_all(
                'div', {'class': 'gd-no', 'fs-cmsfilter-field': 'game-day-number'})[0].text
            row_df['is_game_finished'] = j.find(
                'div', {'class': 'w-embed', 'fs-cmsfilter-field': 'game-over'}).text
            game_date = j.find('h4', {'class': 'g-subheading is-date',
                                'fs-cmssort-field': 'game-date', 'fs-cmssort-type': 'date'}).text
            game_time = j.find_all('h4', {'class': 'g-subheading'})[3].text
            game_time_zone = j.find_all(
                'h4', {'class': 'g-subheading'})[4].text

            gdt = datetime.strptime(
                f"{game_date} {game_time}", "%A, %B %d, %Y %I:%M %p")
            row_df['game_date'] = gdt
            row_df['game_time'] = game_time
            row_df['game_time_zone'] = game_time_zone
            if game_time_zone == "CET":
                row_df['game_date_utc'] = gdt - timedelta(hours=1)
            else:
                row_df['game_date_utc'] = ""

            del gdt, game_time, game_time_zone

            row_df['away_team'] = str(j.find(
                'div', {'class': 'g-team-name-wrap is-left'}).find('h4').text).replace('FehÃ©rvÃ¡r','Fehervar').replace('FEHÉRVÁR','Fehervar')
            row_df['home_team'] = str(j.find(
                'div', {'class': 'g-team-name-wrap is-right'}).find('h4').text).replace('FehÃ©rvÃ¡r','Fehervar').replace('FEHÉRVÁR','Fehervar')

            scores = j.find_all(
                'div', {'class': 'g-score is-real'})
            try:
                row_df['away_score'] = int(scores[0].text)
                row_df['home_score'] = int(scores[1].text)
            except:
                row_df['away_score'] = None
                row_df['home_score'] = None

            game_url = j.find(
                'a', {'class': 'mini-btn w-inline-block'}).get('href')
            row_df['game_url'] = game_url
            row_df['game_id'] = game_url.replace(
                '/live-games/', '').replace('live-games/', '')

            del scores, game_url
            sched_df = pd.concat([sched_df, row_df], ignore_index=True)

        else:
            pass

    ## DEPRICATED
    ## Reason: New website behaves difreriently. 
    # for i in range(1, 4):
    #     normal_url = f"https://europeanleague.football/schedule?92075007_page={i}"
    #     time.sleep(0.5)

    #     response = requests.get(normal_url, headers=headers)
    #     soup = BeautifulSoup(response.text, features='lxml')

    #     games_list = soup.find('div', {'class': 'cms-filter-content'})

    #     games = games_list.find_all(
    #         'div', {"role": "listitem", "class": "w-dyn-item"})

    #     # with open('test.html', 'w+', encoding='latin') as f:
    #     #     f.write(str(games))

    #     del games_list
    #     for j in tqdm(games):
    #         game_season = int(
    #             j.find('div', {'fs-cmsfilter-field': 'season'}).text)

    #         if game_season == season:
    #             row_df = pd.DataFrame({'season': game_season}, index=[0])
    #             row_df['week'] = j.find_all(
    #                 'div', {'class': 'gd-no', 'fs-cmsfilter-field': 'game-day-number'})[0].text
    #             row_df['is_game_finished'] = j.find(
    #                 'div', {'class': 'w-embed', 'fs-cmsfilter-field': 'game-over'}).text
    #             game_date = j.find('h4', {'class': 'g-subheading is-date',
    #                                'fs-cmssort-field': 'game-date', 'fs-cmssort-type': 'date'}).text
    #             game_time = j.find_all('h4', {'class': 'g-subheading'})[3].text
    #             game_time_zone = j.find_all(
    #                 'h4', {'class': 'g-subheading'})[4].text

    #             gdt = datetime.strptime(
    #                 f"{game_date} {game_time}", "%A, %B %d, %Y %I:%M %p")
    #             row_df['game_date'] = gdt
    #             row_df['game_time'] = game_time
    #             row_df['game_time_zone'] = game_time_zone
    #             if game_time_zone == "CET":
    #                 row_df['game_date_utc'] = gdt - timedelta(hours=1)
    #             else:
    #                 row_df['game_date_utc'] = ""

    #             del gdt, game_time, game_time_zone

    #             row_df['away_team'] = str(j.find(
    #                 'div', {'class': 'g-team-name-wrap is-left'}).find('h4').text).replace('FehÃ©rvÃ¡r','Fehervar').replace('FEHÉRVÁR','Fehervar')
    #             row_df['home_team'] = str(j.find(
    #                 'div', {'class': 'g-team-name-wrap is-right'}).find('h4').text).replace('FehÃ©rvÃ¡r','Fehervar').replace('FEHÉRVÁR','Fehervar')

    #             scores = j.find_all(
    #                 'div', {'class': 'g-score is-real'})
    #             try:
    #                 row_df['away_score'] = int(scores[0].text)
    #                 row_df['home_score'] = int(scores[1].text)
    #             except:
    #                 row_df['away_score'] = None
    #                 row_df['home_score'] = None

    #             game_url = j.find(
    #                 'a', {'class': 'mini-btn w-inline-block'}).get('href')
    #             row_df['game_url'] = game_url
    #             row_df['game_id'] = game_url.replace(
    #                 '/live-games/', '').replace('live-games/', '')

    #             del scores, game_url
    #             sched_df = pd.concat([sched_df, row_df], ignore_index=True)

    #         else:
    #             pass



    if save == True:
        sched_df.to_csv(f'schedule/csv/{season}_elf_schedule.csv', index=False)
        sched_df.to_parquet(
            f'schedule/parquet/{season}_elf_schedule.parquet', index=False)

    return sched_df


if __name__ == "__main__":
    get_elf_schedule(return_all_games=True, save=True)

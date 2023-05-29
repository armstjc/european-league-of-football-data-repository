from datetime import datetime, timedelta
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_elf_schedule(season: int, week=0, save=False):
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
    elif week == 0 and get_elf_schedule == False:
        raise ValueError(
            'If `week` is set to 0, set `get_full_schedule` to `True` in order to get the full schedule.')
    elif week > 14:
        raise ValueError(
            '`week` cannot be greater than 14 at this time.')

    for i in range(1, 4):
        normal_url = f"https://europeanleague.football/schedule?92075007_page={i}"
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

    if save == True:
        sched_df.to_csv(f'schedule/csv/{season}_elf_schedule.csv', index=False)
        sched_df.to_parquet(
            f'schedule/parquet/{season}_elf_schedule.parquet', index=False)

    return sched_df


if __name__ == "__main__":
    get_elf_schedule(2023, save=True)

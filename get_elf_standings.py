from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_elf_standings(season: int, save=True):
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
    get_elf_standings(2022, True)

from datetime import datetime
import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def save_elf_game_json(game_id: str):
    """

    """
    game_url = f"https://www.sportsmetrics.football/games/{game_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) " +
        "Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(game_url, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')

    json_string = soup.find(
        'script', {'id': '__NEXT_DATA__', 'type': 'application/json'})

    json_data = json.loads(json_string.text)
    del json_string

    with open(f'raw_game_data/JSON/{game_id}.json', 'w+') as f:
        f.write(json.dumps(json_data['props']['pageProps'], indent=2))

    # print(json_data)
    time.sleep(2)
    return json_data


def save_all_elf_game_json(season: int):
    """

    """
    games_df = pd.read_csv(f'schedule/{season}_elf_schedule.csv')
    # games_df = games_df.dropna(subset=['gamebook_url'])
    games_df = games_df.dropna(subset=["away_team_score", "home_team_score"])
    game_ids_arr = games_df['stats_crew_game_id'].to_numpy()

    for game_id in tqdm(game_ids_arr):
        save_elf_game_json(game_id)


if __name__ == "__main__":
    now = datetime.now()
    save_all_elf_game_json(now.year)

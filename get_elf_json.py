import json
# import logging
import time
from datetime import datetime

import pandas as pd
import requests
# from bs4 import BeautifulSoup
from tqdm import tqdm


def save_elf_game_json(game_id: str):
    """

    """
    game_url = f"https://europeanleague.football/api/game/{game_id}/xml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) " +
        "Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(game_url, headers=headers)
    json_data = json.loads(response.text)

    with open(f'raw_game_data/JSON/{game_id}.json', 'w+') as f:
        f.write(json.dumps(json_data, indent=2))

    time.sleep(2)
    return json_data


def save_all_elf_game_json(season: int):
    """

    """
    games_df = pd.read_csv(f'schedule/{season}_elf_schedule.csv')
    games_df = games_df[games_df["has_game_started"]]
    game_ids_arr = games_df['sports_metrics_game_id'].to_numpy()

    for game_id in tqdm(game_ids_arr):
        save_elf_game_json(game_id)


if __name__ == "__main__":
    now = datetime.now()
    save_all_elf_game_json(now.year)
    # save_all_elf_game_json(2024)

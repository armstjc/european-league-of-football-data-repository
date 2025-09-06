import json
import time
from datetime import datetime
import re
from os.path import exists
import pandas as pd
import requests
from tqdm import tqdm


def save_elf_game_json(old_game_id: str, game_id: str, force_reload: bool = False):
    """

    """
    # game_url = f"https://europeanleague.football/api/game/{game_id}/xml"
    game_url = f"https://europeanleague.football/games/{old_game_id}?_rsc=sdpt8"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) " +
        "Chrome/114.0.0.0 Safari/537.36"
    }

    if (
        exists(f'raw_game_data/json/{game_id}.json') and
        force_reload is False
    ):
        with open(f'raw_game_data/json/{game_id}.json', 'r') as f:
            json_str = f.read()
        json_data = json.loads(json_str)
        return json_data

    response = requests.get(game_url, headers=headers)
    # json_data = json.loads(response.text)

    # with open(f'raw_game_data/json/{game_id}.json', 'w+') as f:
    #     f.write(json.dumps(json_data, indent=2))
    # time.sleep(2)
    # return json_data

    # json_str = json_str.replace("\\\"","\"")
    # with open("test.html", "w+", encoding="latin1", errors="ignore") as f:
    #     f.write(response.text)

    json_str = re.findall(
        r"(\{\\\"gameData\\\"\:\[.+)\]\}\]\\n\"\]\)\<\/script\>",
        response.text
    )[0]
    json_str = json_str.replace("\\\"", "\"")
    json_str = json_str.replace(": \"NA\"", ": 0")
    json_data = json.loads(json_str)
    player_data = json_data["playerData"]
    json_data = json_data["gameData"][0]
    xml_data = json_data["xmlInfo"]
    xml_data["playerData"] = player_data
    with open(f'raw_game_data/json/{game_id}.json', 'w+') as f:
        f.write(json.dumps(xml_data, indent=2))
    time.sleep(2)
    return json_data


def save_all_elf_game_json(season: int):
    """

    """
    games_df = pd.read_csv(f'schedule/{season}_elf_schedule.csv')
    games_df = games_df[games_df["has_game_started"]]
    game_ids_arr = games_df['sports_metrics_game_id'].to_numpy()
    old_game_ids_arr = games_df['old_game_id'].to_numpy()

    for i in tqdm(range(0, len(game_ids_arr))):
        game_id = game_ids_arr[i]
        old_game_id = old_game_ids_arr[i]
        save_elf_game_json(
            old_game_id=old_game_id,
            game_id=game_id,
            force_reload=False
        )


if __name__ == "__main__":
    now = datetime.now()
    save_all_elf_game_json(now.year)

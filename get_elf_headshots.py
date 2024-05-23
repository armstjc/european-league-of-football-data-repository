from datetime import datetime
import logging
import time
import urllib.request
import pandas as pd
from tqdm import tqdm


def get_elf_player_headshots(season: int):
    sched_df = pd.read_csv(f'rosters/{season}_elf_rosters.csv')

    sched_df = sched_df.dropna(subset=['player_headshot_url'])

    player_id_arr = sched_df['player_id'].to_numpy()
    headshot_url_arr = sched_df['player_headshot_url'].to_numpy()

    for i in tqdm(range(0, len(player_id_arr))):
        player_id = player_id_arr[i]
        headshot_url = headshot_url_arr[i]
        photo_filepath = f"player_info/photos/{player_id}.jpg"

        try:
            urllib.request.urlretrieve(headshot_url, filename=photo_filepath)
        except Exception as e:
            logging.warning(
                f'Could not get the player headshot for {player_id}. ' +
                f"Full exception `{e}`."
            )
            time.sleep(4)

        time.sleep(3)


if __name__ == "__main__":
    now = datetime.now()
    get_elf_player_headshots(now.year)

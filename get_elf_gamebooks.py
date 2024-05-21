import logging
import urllib.request
from datetime import datetime

import pandas as pd
from tqdm import tqdm


def get_elf_game_books(season: int):
    sched_df = pd.read_csv(f'schedule/{season}_elf_schedule.csv')

    sched_df = sched_df.dropna(subset=['gamebook_url'])

    game_books_arr = sched_df['gamebook_url'].to_numpy()
    old_game_id_arr = sched_df['old_game_id'].to_numpy()

    for i in tqdm(range(0, len(game_books_arr))):
        url = game_books_arr[i]
        game_id = old_game_id_arr[i]
        pdf_filepath = f"gamebooks/{game_id}.pdf"

        try:
            urllib.request.urlretrieve(url, filename=pdf_filepath)
        except Exception as e:
            logging.warning(
                f'Could not get the game book for {game_id}. ' +
                f"Full exception: `{e}`"
            )


if __name__ == "__main__":
    now = datetime.now()
    get_elf_game_books(now.year)

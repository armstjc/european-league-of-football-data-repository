import urllib.request
import pandas as pd
from tqdm import tqdm


def get_elf_gamebooks(season: int):
    sched_df = pd.read_csv(f'schedule/{season}_elf_schedule.csv')

    sched_df = sched_df.dropna(subset=['gamebook_url'])

    gamebooks_arr = sched_df['gamebook_url'].to_numpy()
    old_game_id_arr = sched_df['old_game_id'].to_numpy()

    for i in tqdm(range(0, len(gamebooks_arr))):
        url = gamebooks_arr[i]
        game_id = old_game_id_arr[i]
        pdf_filepath = f"gamebooks/{game_id}.pdf"

        try:
            urllib.request.urlretrieve(url, filename=pdf_filepath)
        except:
            print(f'Could not get the game book for {game_id}.')


if __name__ == "__main__":
    get_elf_gamebooks(2023)

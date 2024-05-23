from datetime import datetime

from get_elf_schedule import get_elf_schedule


def get_elf_game_pbp_json(game_id: str):
    """

    """
    


def get_season_elf_pbp_json(season: int):
    """

    """
    now = datetime.now()
    if season < 2021:
        raise ValueError('`season` cannot be less than 2021.')
    elif season > now.year:
        raise ValueError(f'`season` cannot be greater than {now.year}')

    schedule_df = get_elf_schedule(season_filter=season)
    game_id_arr = schedule_df['game_id'].to_numpy()

    print('')
    for j in game_id_arr:
        get_elf_game_pbp_json(j)


if __name__ == "__main__":
    get_season_elf_pbp_json(2023)

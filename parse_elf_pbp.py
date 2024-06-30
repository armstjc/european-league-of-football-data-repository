import logging
import os
import time
# from datetime import datetime
from random import randrange

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

from get_elf_schedule import get_elf_schedule


def get_efl_raw_pbp(season: int, overwrite_existing_cache: bool = False):
    """

    """
    # now = datetime.now()

    schedule_df = get_elf_schedule(season_filter=season)
    schedule_df = schedule_df.loc[
        schedule_df["has_game_started"] == True  # noqa: E712
    ]
    schedule_df = schedule_df.loc[
        schedule_df["is_cancelled"] == False  # noqa: E712
    ]
    week_arr = schedule_df["week"].to_numpy()
    game_id_arr = schedule_df["game_id"].to_numpy()
    game_datetime_arr = schedule_df["date"].to_numpy()

    away_team_id_arr = schedule_df["away_team_id"].to_numpy()
    away_team_slug_arr = schedule_df["away_team_slug"].to_numpy()

    home_team_id_arr = schedule_df["home_team_id"].to_numpy()
    home_team_slug_arr = schedule_df["home_team_slug"].to_numpy()
    # response = requests.get(url=url)

    driver = webdriver.Chrome()

    for i in tqdm(range(0, len(game_id_arr))):
        # with open("test.html", "w+", encoding="utf-8") as f:
        #     f.write(response.text)

        pbp_df = pd.DataFrame()
        pbp_df_arr = []

        temp_df = pd.DataFrame()

        game_week = week_arr[i]
        game_id = game_id_arr[i]
        game_datetime = game_datetime_arr[i]

        away_team = away_team_slug_arr[i]
        away_team_id = away_team_id_arr[i]

        home_team = home_team_slug_arr[i]
        home_team_id = home_team_id_arr[i]

        if os.path.exists(f"pbp/raw/{game_id}.csv") \
                and overwrite_existing_cache is False:
            pass
        else:
            url = "https://europeanleague.football/game-center/schedule/" +\
                f"{away_team}-at-{home_team}-{game_id}"
            driver.get(url)
            time.sleep(10)
            has_pbp_data = False

            rand_num = randrange(1000, 3000)
            driver.execute_script(f"window.scrollBy(0,{rand_num})", "")
            soup = BeautifulSoup(driver.page_source, features='lxml')

            try:
                pbp_data = soup.find(
                    "div", {"class": "@container flex flex-col gap-12"}
                )
                has_pbp_data = True
            except:
                logging.info(
                    "No PBP data was found, skipping this game"
                )

            if has_pbp_data is True:
                quarters = pbp_data.find_all(
                    "div", {"class": "flex flex-col gap-6"}
                )

                quarter_num = 0
                for q in quarters:
                    quarter_num += 1
                    drives = q.find_all(
                        "div",
                        {
                            "class": "relative rounded-xl " +
                            "overflow-hidden duration-200 " +
                            "bg-elf-blue-800 lg:hover:bg-elf-blue-700/70"
                        }
                    )

                    drive_num = 0
                    for d in drives:
                        drive_num += 1
                        plays = d.find_all(
                            "div",
                            {
                                "class": "px-4 md:px-6 py-4 " +
                                "border-t border-elf-blue-200/30"
                            }
                        )

                        for p in plays:
                            play_type = p.find(
                                "p",
                                {
                                    "class": "text-lg font-bold " +
                                    "mb-1 leading-normal"
                                }
                            ).text
                            play_desc = p.find("p", {"class": "text-sm mb-1"}).text
                            down_and_distance = p.find(
                                "p", {"class": "text-sm text-elf-blue-100/70"}
                            ).text

                            temp_df = pd.DataFrame(
                                {
                                    "season": season,
                                    "game_week": game_week,
                                    "game_datetime": game_datetime,
                                    "away_team": away_team,
                                    "away_team_id": away_team_id,
                                    "home_team": home_team,
                                    "home_team_id": home_team_id,
                                    "quarter_num": quarter_num,
                                    "drive_num": drive_num,
                                    "play_type": play_type,
                                    "play_desc": play_desc,
                                    "down_and_distance": down_and_distance,
                                },
                                index=[0]
                            )

                            pbp_df_arr.append(temp_df)

                            del temp_df

            if len(pbp_df_arr) == 0:
                pass
            elif len(pbp_df_arr) > 0:
                pbp_df = pd.concat(pbp_df_arr, ignore_index=True)
                pbp_df.to_csv(
                    f"pbp/raw/{game_id}.csv",
                    index=False
                )


if __name__ == "__main__":
    get_efl_raw_pbp(
        2024,
        # overwrite_existing_cache=True
    )

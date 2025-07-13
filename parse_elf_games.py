import json
import logging

import numpy as np
import pandas as pd
from tqdm import tqdm

from elf_utils import get_json_in_folder


def parse_raw_elf_pbp():
    """ """
    json_list = get_json_in_folder("raw_game_data/json")


def parse_elf_player_stats(json_data: dict) -> pd.DataFrame:
    """ """
    stat_columns = [
        "game_id",
        "game_date",
        "game_location",
        "game_stadium",
        "away_abv",
        "away_name",
        "home_abv",
        "home_name",
        "team_id",
        "team_name",
        "visitor_home",
        "player_code",
        "player_jersey_num",
        "player_name",
        "player_short_name",
        "player_check_name",
        "player_position",
        "GP",
        "GS",

        "pass_comp",
        "pass_att",
        "pass_yds",
        "pass_td",
        "pass_int",
        "pass_long",
        "pass_sacks",
        "pass_sack_yds",

        "rush_att",
        "rush_yds",
        "rush_yds_gain",
        "rush_yds_loss",
        "rush_td",
        "rush_long",

        "receiving_rec",
        "receiving_yds",
        "receiving_td",
        "receiving_long",

        "fumbles_num",
        "fumbles_lost",

        "defense_tackles_total",
        "defense_tackles_solo",
        "defense_tackles_ast",
        "defense_tfl_solo",
        "defense_tfl_ast",
        "defense_tfl",
        "defense_tfl_YDS",
        "defense_sacks",
        "defense_sack_yds",
        "defense_interceptions_num",
        "defense_interceptions_yds",
        "defense_interceptions_td",
        "defense_interceptions_long",
        "defense_pbu",
        "defense_fr",
        "defense_fr_yds",
        "defense_fr_td",
        "defense_fr_long",

        "kick_return_num",
        "kick_return_yds",
        "kick_return_td",
        "kick_return_long",

        "punt_return_num",
        "punt_return_yds",
        "punt_return_td",
        "punt_return_long",

        "kickoff_att",
        "kickoff_yds",
        "kickoff_out_of_bounds",
        "kickoff_tb",

        "punt_att",
        "punt_gross_yds",
        "punt_long",
        "punt_blk",
        "punt_tb",
        "punt_fc",
        "punt_50+",
        "punt_in_20",
        "punt_gross_avg",

        "kick_fgm",
        "kick_fga",
        "kick_fg%",
        "kick_fg_long",
        "kick_fg_blk",
        "kick_xpm",
        "kick_xpa",
        "kick_xp%",
        "2PM_pass_att",
        "2PM_pass_made",

        "field_goal_return_num",
        "field_goal_return_yds",
        "field_goal_return_td"
    ]

    data_df_arr = []
    data_df = pd.DataFrame()

    json_data = json_data["fbgame"]
    game_id = json_data["venue"]["_attributes"]["gameid"]
    game_date = json_data["venue"]["_attributes"]["date"]

    game_date += "T" + json_data["venue"]["_attributes"]["start"]
    game_date = game_date.replace(">", ":")
    game_date = game_date.replace("T19H", "T19:00")
    game_date = game_date.replace("T19h", "T19:00")
    game_date = game_date.replace("T18.00", "T18:00")

    game_location = json_data["venue"]["_attributes"]["location"]
    game_stadium = json_data["venue"]["_attributes"]["stadium"]

    away_abv = json_data["venue"]["_attributes"]["visid"]
    home_abv = json_data["venue"]["_attributes"]["homeid"]
    away_name = json_data["venue"]["_attributes"]["visname"]
    home_name = json_data["venue"]["_attributes"]["homename"]

    for team in json_data["team"]:
        team_id = team["_attributes"]["id"]
        team_name = team["_attributes"]["name"]
        visitor_home = team["_attributes"]["vh"]

        if "player" not in team:
            continue
        for player in team["player"]:
            temp_df = pd.DataFrame(
                {
                    "game_id": game_id,
                    "game_date": game_date,
                    "game_location": game_location,
                    "game_stadium": game_stadium,
                    "away_abv": away_abv,
                    "away_name": away_name,
                    "home_abv": home_abv,
                    "home_name": home_name,
                    "team_id": team_id,
                    "team_name": team_name,
                    "visitor_home": visitor_home,
                    "player_id": None
                },
                index=[0],
            )
            if "player" in team:
                pass
            else:
                return temp_df

            for key, value in player.items():
                if key == "_attributes":
                    temp_df["player_code"] = value["code"]
                    temp_df["player_jersey_num"] = value["uni"]
                    temp_df["player_name"] = value["name"]
                    player_name = value["name"]
                    temp_df["player_short_name"] = value["shortname"]
                    temp_df["player_check_name"] = value["checkname"]

                    try:
                        temp_df["player_id"] = value["id"]
                    except Exception:
                        logging.info(
                            f"No player ID found for {player_name}"
                        )

                    try:
                        temp_df["player_position"] = value["opos"]
                    except Exception:
                        temp_df["player_position"] = np.nan
                        logging.info(
                            "Skipping player position check for this player."
                        )
                    temp_df["GP"] = int(value["gp"])
                    try:
                        temp_df["GS"] = int(value["gs"])
                    except Exception:
                        temp_df["GS"] = 0
                        logging.info("Player did not start this game.")
                elif key == "rush":
                    if value == {}:
                        continue
                    elif value["_attributes"] == {'att': '', 'yds': '', 'gain': '', 'loss': '', 'td': '', 'long': ''}:
                        continue

                    temp_df["rush_att"] = int(value["_attributes"]["att"])
                    temp_df["rush_yds"] = int(value["_attributes"]["yds"])

                    try:
                        temp_df["rush_yds_gain"] = int(value["_attributes"]["gain"])
                    except Exception:
                        temp_df["rush_yds_gain"] = np.nan
                        logging.info(
                            f"No rush yards gain data found for {team_name} in `{game_id}`."
                        )

                    try:
                        if value["_attributes"]["loss"] == "":
                            value["_attributes"]["loss"] = 0
                        temp_df["rush_yds_loss"] = int(value["_attributes"]["loss"])
                    except Exception:
                        temp_df["rush_yds_loss"] = np.nan
                        logging.info(
                            f"No rush yards loss data found for {team_name} in `{game_id}`."
                        )

                    temp_df["rush_td"] = int(value["_attributes"]["td"])
                    try:
                        temp_df["rush_long"] = int(value["_attributes"]["long"])
                    except Exception:
                        temp_df["rush_long"] = np.nan
                        logging.info(
                            f"No rush long data found for {team_name} in `{game_id}`."
                        )
                elif key == "pass":
                    if value == {}:
                        continue
                    elif value["_attributes"] == {'comp': '', 'att': '', 'yds': '', 'td': '', 'int': '', 'long': '', 'sack': '', 'sack_yds': ''}:
                        continue
                    temp_df["pass_comp"] = int(value["_attributes"]["comp"])
                    temp_df["pass_att"] = int(value["_attributes"]["att"])
                    temp_df["pass_yds"] = int(value["_attributes"]["yds"])
                    temp_df["pass_td"] = int(value["_attributes"]["td"])
                    temp_df["pass_int"] = int(value["_attributes"]["int"])
                    try:
                        temp_df["pass_long"] = int(value["_attributes"]["long"])
                    except Exception:
                        temp_df["pass_long"] = np.nan
                        logging.info(
                            f"No pass long data found for {team_name} in `{game_id}`."
                        )
                    if value["_attributes"]["sacks"] == "":
                        value["_attributes"]["sacks"] = 0
                    temp_df["pass_sacks"] = int(value["_attributes"]["sacks"])
                    if value["_attributes"]["sackyds"] == "":
                        value["_attributes"]["sackyds"] = 0
                    temp_df["pass_sack_yds"] = int(value["_attributes"]["sackyds"])

                elif key == "rcv":
                    if value == {}:
                        continue

                    try:
                        temp_df["receiving_rec"] = int(value["_attributes"]["no"])
                    except Exception:
                        temp_df["receiving_rec"] = np.nan
                        logging.info(
                            f"No receiving long data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["receiving_yds"] = int(value["_attributes"]["yds"])
                    except Exception:
                        temp_df["receiving_yds"] = np.nan
                        logging.info(
                            f"No receiving long data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["receiving_td"] = int(value["_attributes"]["td"])
                    except Exception:
                        temp_df["receiving_td"] = np.nan
                        logging.info(
                            f"No receiving long data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["receiving_long"] = int(value["_attributes"]["long"])
                    except Exception:
                        temp_df["receiving_long"] = np.nan
                        logging.info(
                            f"No receiving long data found for {team_name} in `{game_id}`."
                        )
                elif key == "punt":
                    if value == {}:
                        continue
                    elif value["_attributes"] == {'no': '', 'yds': '', 'long': '', 'blk': ''}:
                        continue
                    temp_df["punt_att"] = int(value["_attributes"]["no"])
                    temp_df["punt_gross_yds"] = int(value["_attributes"]["yds"])
                    temp_df["punt_long"] = int(value["_attributes"]["long"])
                    temp_df["punt_blk"] = int(value["_attributes"]["blkd"])
                    temp_df["punt_tb"] = int(value["_attributes"]["tb"])
                    temp_df["punt_fc"] = int(value["_attributes"]["fc"])
                    temp_df["punt_50+"] = int(value["_attributes"]["plus50"])
                    temp_df["punt_in_20"] = int(value["_attributes"]["inside20"])
                    temp_df["punt_gross_avg"] = (
                        temp_df["punt_gross_yds"] / temp_df["punt_att"]
                    )
                    temp_df["punt_gross_avg"] = temp_df["punt_gross_avg"].round(3)
                elif key == "ko":
                    if value == {}:
                        continue
                    temp_df["kickoff_att"] = int(value["_attributes"]["no"])
                    temp_df["kickoff_yds"] = int(value["_attributes"]["yds"])
                    temp_df["kickoff_out_of_bounds"] = int(value["_attributes"]["ob"])
                    temp_df["kickoff_tb"] = int(value["_attributes"]["tb"])
                elif key == "pat":
                    if value == {}:
                        continue
                    try:
                        temp_df["kick_xpm"] = int(value["_attributes"]["kickmade"])
                    except Exception:
                        temp_df["kick_xpm"] = 0
                        logging.info(
                            f"No XPM data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["kick_xpa"] = int(value["_attributes"]["kickatt"])
                    except Exception:
                        temp_df["kick_xpa"] = 0
                        logging.info(
                            f"No XPM data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["2PM_pass_att"] = int(value["_attributes"]["passatt"])
                    except Exception:
                        temp_df["2PM_pass_att"] = 0
                        logging.info(
                            f"No 2PA data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["2PM_pass_made"] = int(value["_attributes"]["passmade"])
                    except Exception:
                        temp_df["2PM_pass_made"] = 0
                        logging.info(
                            f"No 2PT data found for {team_name} in `{game_id}`."
                        )
                    if temp_df["kick_xpa"].iloc[0] != 0:
                        temp_df["kick_xp%"] = temp_df["kick_xpm"] / temp_df["kick_xpa"]
                        temp_df["kick_xp%"] = temp_df["kick_xp%"].round(3)
                elif key == "xp":
                    if value == {}:
                        continue
                    try:
                        temp_df["kick_xpm"] = int(value["_attributes"]["made"])
                    except Exception:
                        temp_df["kick_xpm"] = 0
                        logging.info(
                            f"No XPM data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["kick_xpa"] = int(value["_attributes"]["att"])
                    except Exception:
                        temp_df["kick_xpa"] = 0
                        logging.info(
                            f"No XPM data found for {team_name} in `{game_id}`."
                        )

                elif key == "def":
                    if value == {}:
                        continue

                    try:
                        temp_df["defense_tackles_total"] = int(
                            value["_attributes"]["tot_tack"]
                        )
                    except Exception:
                        temp_df["defense_tackles_solo"] = np.nan
                        logging.info(
                            f"No TOTAL data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_tackles_solo"] = int(
                            value["_attributes"]["tackua"]
                        )
                    except Exception:
                        temp_df["defense_tackles_solo"] = np.nan
                        logging.info(
                            f"No SOLO data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_tackles_ast"] = int(
                            value["_attributes"]["tacka"]
                        )
                    except Exception:
                        temp_df["defense_tackles_ast"] = np.nan
                        logging.info(
                            f"No AST data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_tfl_solo"] = int(value["_attributes"]["tflua"])
                    except Exception:
                        temp_df["defense_tfl_solo"] = np.nan
                        logging.info(
                            f"No SOLO TFL data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["defense_tfl_ast"] = int(value["_attributes"]["tfla"])
                    except Exception:
                        temp_df["defense_tfl_ast"] = np.nan
                        logging.info(
                            f"No AST TFL data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["defense_tfl"] = temp_df["defense_tfl_solo"] + (
                            temp_df["defense_tfl_ast"] / 2
                        )
                        temp_df["defense_tfl"] = temp_df["defense_tfl"].round(1)
                    except Exception:
                        temp_df["defense_tfl"] = np.nan
                        logging.info(
                            f"No TFL data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["defense_tfl_YDS"] = int(value["_attributes"]["tflyds"])
                    except Exception:
                        temp_df["defense_tfl_YDS"] = np.nan
                        logging.info(
                            f"No TFL yds data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_sacks"] = int(value["_attributes"]["sacks"])
                    except Exception:
                        temp_df["defense_sacks"] = np.nan
                        logging.info(
                            f"No sack data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_sack_yds"] = int(value["_attributes"]["sacks"])
                    except Exception:
                        temp_df["defense_sack_yds"] = np.nan
                        logging.info(
                            f"No sack yds data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["defense_pbu"] = int(value["_attributes"]["brup"])
                    except Exception:
                        temp_df["defense_pbu"] = np.nan
                        logging.info(
                            f"No PBU data found for {team_name} in `{game_id}`."
                        )
                elif key == "defense":
                    if value == {}:
                        continue

                    try:
                        temp_df["defense_tackles_total"] = int(
                            value["_attributes"]["tot_tack"]
                        )
                    except Exception:
                        temp_df["defense_tackles_solo"] = np.nan
                        logging.info(
                            f"No TOTAL data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_tackles_solo"] = int(
                            value["_attributes"]["tackua"]
                        )
                    except Exception:
                        temp_df["defense_tackles_solo"] = np.nan
                        logging.info(
                            f"No SOLO data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_tackles_ast"] = int(
                            value["_attributes"]["tacka"]
                        )
                    except Exception:
                        temp_df["defense_tackles_ast"] = np.nan
                        logging.info(
                            f"No AST data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_tfl_solo"] = int(value["_attributes"]["tflua"])
                    except Exception:
                        temp_df["defense_tfl_solo"] = np.nan
                        logging.info(
                            f"No SOLO TFL data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["defense_tfl_ast"] = int(value["_attributes"]["tfla"])
                    except Exception:
                        temp_df["defense_tfl_ast"] = np.nan
                        logging.info(
                            f"No AST TFL data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["defense_tfl"] = temp_df["defense_tfl_solo"] + (
                            temp_df["defense_tfl_ast"] / 2
                        )
                        temp_df["defense_tfl"] = temp_df["defense_tfl"].round(1)
                    except Exception:
                        temp_df["defense_tfl"] = np.nan
                        logging.info(
                            f"No TFL data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["defense_tfl_YDS"] = int(value["_attributes"]["tflyds"])
                    except Exception:
                        temp_df["defense_tfl_YDS"] = np.nan
                        logging.info(
                            f"No TFL yds data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_sacks"] = int(value["_attributes"]["sacks"])
                    except Exception:
                        temp_df["defense_sacks"] = np.nan
                        logging.info(
                            f"No sack data found for {team_name} in `{game_id}`."
                        )
                    try:
                        temp_df["defense_sack_yds"] = int(value["_attributes"]["sacks"])
                    except Exception:
                        temp_df["defense_sack_yds"] = np.nan
                        logging.info(
                            f"No sack yds data found for {team_name} in `{game_id}`."
                        )

                    try:
                        temp_df["defense_pbu"] = int(value["_attributes"]["brup"])
                    except Exception:
                        temp_df["defense_pbu"] = np.nan
                        logging.info(
                            f"No PBU data found for {team_name} in `{game_id}`."
                        )
                elif key == "kr":
                    if value == {}:
                        continue
                    elif value["_attributes"] == {'no': '', 'yds': '', 'td': '', 'long': ''}:
                        continue
                    temp_df["kick_return_num"] = int(value["_attributes"]["no"])
                    temp_df["kick_return_yds"] = int(value["_attributes"]["yds"])
                    temp_df["kick_return_td"] = int(value["_attributes"]["td"])
                    temp_df["kick_return_long"] = int(value["_attributes"]["long"])
                elif key == "pr":
                    if value == {}:
                        continue
                    elif value["_attributes"] == {'no': '', 'yds': '', 'td': '', 'long': ''}:
                        continue
                    temp_df["punt_return_num"] = int(value["_attributes"]["no"])
                    temp_df["punt_return_yds"] = int(value["_attributes"]["yds"])
                    temp_df["punt_return_td"] = int(value["_attributes"]["td"])
                    temp_df["punt_return_long"] = int(value["_attributes"]["long"])
                elif key == "ir":
                    if value == {}:
                        continue
                    temp_df["defense_interceptions_num"] = int(
                        value["_attributes"]["no"]
                    )
                    temp_df["defense_interceptions_yds"] = int(
                        value["_attributes"]["yds"]
                    )
                    temp_df["defense_interceptions_td"] = int(
                        value["_attributes"]["td"]
                    )
                    temp_df["defense_interceptions_long"] = int(
                        value["_attributes"]["long"]
                    )
                elif key == "fg":
                    if value == {}:
                        continue
                    elif value["_attributes"] == {'att': '', 'made': '', 'long': ''}:
                        continue
                    temp_df["kick_fgm"] = int(value["_attributes"]["made"])
                    temp_df["kick_fga"] = int(value["_attributes"]["att"])
                    temp_df["kick_fg%"] = temp_df["kick_fgm"] / temp_df["kick_fga"]
                    temp_df["kick_fg%"] = temp_df["kick_fg%"].round(3)
                    temp_df["kick_fg_long"] = int(value["_attributes"]["long"])
                    temp_df["kick_fg_blk"] = int(value["_attributes"]["blkd"])
                elif key == "fr":
                    if value == {}:
                        continue
                    temp_df["defense_fr"] = int(value["_attributes"]["no"])
                    temp_df["defense_fr_yds"] = int(value["_attributes"]["yds"])
                    temp_df["defense_fr_td"] = int(value["_attributes"]["td"])
                    temp_df["defense_fr_long"] = int(value["_attributes"]["long"])
                elif key == "fgr":
                    temp_df["field_goal_return_num"] = int(value["_attributes"]["no"])
                    temp_df["field_goal_return_yds"] = int(value["_attributes"]["yds"])
                    try:
                        temp_df["field_goal_return_td"] = int(
                            value["_attributes"]["td"]
                        )
                    except Exception:
                        temp_df["field_goal_return_td"] = 0
                        logging.info(
                            f"No FG return TD data found for {team_name} in `{game_id}`."
                        )
                elif key == "fumbles":
                    if value == {}:
                        continue
                    temp_df["fumbles_num"] = int(value["_attributes"]["no"])
                    temp_df["fumbles_lost"] = int(value["_attributes"]["lost"])
                elif key == "scoring":
                    pass
                else:
                    raise KeyError(f"Unhandled key `{key}`.")
            temp_df = temp_df.infer_objects()
            data_df_arr.append(temp_df)
            del temp_df

    if len(data_df_arr) == 0:
        return data_df
    data_df = pd.concat(data_df_arr, ignore_index=True)
    data_df["game_date"] = pd.to_datetime(data_df["game_date"], format="%m/%d/%YT%H:%M")
    data_df["season"] = data_df["game_date"].dt.year
    return data_df


def parse_elf_team_stats(json_data: dict) -> pd.DataFrame:
    """ """
    data_df_arr = []
    stat_columns = [
        "game_id",
        "game_date",
        "game_location",
        "game_stadium",
        "away_abv",
        "away_name",
        "home_abv",
        "home_name",
        "team_id",
        "team_name",
        "visitor_home",
        "total_plays",
        "total_yds",
        "total_yds_per_play",
        "first_downs_total",
        "first_downs_pass",
        "first_downs_rush",
        "first_downs_penalty",
        "penalties_num",
        "penalties_yds",
        "third_down_conv",
        "third_down_att",
        "fourth_down_conv",
        "fourth_down_att",
        "fumbles_num",
        "fumbles_lost",
        "misc_yds",
        "time_of_possession",
        "points_off_turnovers",
        "redzone_att",
        "redzone_scores",
        "redzone_points",
        "redzone_rush_td",
        "redzone_pass_td",
        "redzone_fgm",
        "redzone_end_fga",
        "redzone_end_downs",
        "redzone_end_int",
        "redzone_end_fumble",
        "redzone_end_half",
        "redzone_end_game",
        "pass_comp",
        "pass_att",
        "pass_yds",
        "pass_td",
        "pass_int",
        "pass_long",
        "rush_att",
        "rush_yds",
        "rush_yds_gain",
        "rush_yds_loss",
        "rush_td",
        "rush_long",
        "defense_tackles_total",
        "defense_tackles_solo",
        "defense_tackles_ast",
        "defense_tfl_solo",
        "defense_tfl_ast",
        "defense_tfl",
        "defense_tfl_YDS",
        "defense_sacks",
        "defense_sack_yds",
        "defense_interceptions_num",
        "defense_interceptions_yds",
        "defense_interceptions_td",
        "defense_interceptions_long",
        "defense_pbu",
        "defense_fr",
        "defense_fr_yds",
        "defense_fr_td",
        "defense_fr_long",
        "punt_att",
        "punt_gross_yds",
        "punt_long",
        "punt_blk",
        "punt_tb",
        "punt_fc",
        "punt_50+",
        "punt_in_20",
        "punt_gross_avg",
        "kickoff_att",
        "kickoff_yds",
        "kickoff_out_of_bounds",
        "kickoff_tb",
        "kick_fgm",
        "kick_fga",
        "kick_fg%",
        "kick_fg_long",
        "kick_fg_blk",
        "kick_xpm",
        "kick_xpa",
        "kick_xp%",
        "2PM_pass_att",
        "2PM_pass_made",
        "kick_return_num",
        "kick_return_yds",
        "kick_return_td",
        "kick_return_long",
        "punt_return_num",
        "punt_return_yds",
        "punt_return_td",
        "punt_return_long",
        "field_goal_return_num",
        "field_goal_return_yds",
        "field_goal_return_td",
    ]

    data_df = pd.DataFrame()

    json_data = json_data["fbgame"]
    game_id = json_data["venue"]["_attributes"]["gameid"]
    game_date = json_data["venue"]["_attributes"]["date"]
    game_location = json_data["venue"]["_attributes"]["location"]
    game_stadium = json_data["venue"]["_attributes"]["stadium"]

    away_abv = json_data["venue"]["_attributes"]["visid"]
    home_abv = json_data["venue"]["_attributes"]["homeid"]
    away_name = json_data["venue"]["_attributes"]["visname"]
    home_name = json_data["venue"]["_attributes"]["homename"]

    for team in json_data["team"]:
        temp_df = pd.DataFrame(
            {
                "game_id": game_id,
                "game_date": game_date,
                "game_location": game_location,
                "game_stadium": game_stadium,
                "away_abv": away_abv,
                "away_name": away_name,
                "home_abv": home_abv,
                "home_name": home_name,
                "team_id": None,
                "team_name": None,
                "visitor_home": None,
            },
            index=[0],
        )
        temp_df["team_id"] = team["_attributes"]["id"]
        team_name = team["_attributes"]["name"]
        temp_df["team_name"] = team_name
        temp_df["visitor_home"] = team["_attributes"]["vh"]
        for key, value in team["totals"].items():
            if key == "_attributes":
                if value == {}:
                    continue
                temp_df["total_plays"] = int(value["totoff_plays"])
                temp_df["total_yds"] = int(value["totoff_yards"])
                temp_df["total_yds_per_play"] = (
                    temp_df["total_yds"] / temp_df["total_plays"]
                )
            elif key == "firstdowns":
                if value == {}:
                    continue
                temp_df["first_downs_total"] = int(value["_attributes"]["no"])
                temp_df["first_downs_pass"] = int(value["_attributes"]["pass"])
                temp_df["first_downs_rush"] = int(value["_attributes"]["rush"])
                temp_df["first_downs_penalty"] = int(value["_attributes"]["penalty"])
            elif key == "penalties":
                if value == {}:
                    continue
                temp_df["penalties_num"] = int(value["_attributes"]["no"])
                temp_df["penalties_yds"] = int(value["_attributes"]["yds"])
            elif key == "conversions":
                if value == {}:
                    continue
                temp_df["third_down_conv"] = int(value["_attributes"]["thirdconv"])
                temp_df["third_down_att"] = int(value["_attributes"]["thirdatt"])
                temp_df["fourth_down_conv"] = int(value["_attributes"]["fourthconv"])
                temp_df["fourth_down_att"] = int(value["_attributes"]["fourthatt"])
            elif key == "fumbles":
                if value == {}:
                    continue
                temp_df["fumbles_num"] = int(value["_attributes"]["no"])
                temp_df["fumbles_lost"] = int(value["_attributes"]["lost"])
            elif key == "misc":
                if value == {}:
                    continue
                try:
                    temp_df["misc_yds"] = int(value["_attributes"]["yds"])
                except Exception:
                    temp_df["misc_yds"] = 0
                    logging.info(
                        f"No misc. yds data found for {team_name} in `{game_id}`."
                    )
                try:
                    temp_df["time_of_possession"] = value["_attributes"]["top"]
                except Exception:
                    temp_df["misc_yds"] = 0
                    logging.info(f"No TOP data found for {team_name} in `{game_id}`.")

                try:
                    if value["_attributes"]["ptsto"] == "":
                        value["_attributes"]["ptsto"] = 0
                    temp_df["points_off_turnovers"] = int(value["_attributes"]["ptsto"])
                except Exception:
                    temp_df["points_off_turnovers"] = 0
                    logging.info(
                        f"No points off turnovers data found for {team_name} in `{game_id}`."
                    )
            elif key == "fumbles":
                if value == {}:
                    continue
                temp_df["fumbles_num"] = int(value["_attributes"]["no"])
                temp_df["fumbles_lost"] = int(value["_attributes"]["lost"])
            elif key == "redzone":
                if value == {}:
                    continue
                temp_df["redzone_att"] = int(value["_attributes"]["att"])
                temp_df["redzone_scores"] = int(value["_attributes"]["scores"])
                try:
                    temp_df["redzone_points"] = int(value["_attributes"]["points"])
                except Exception:
                    temp_df["redzone_points"] = 0

                try:
                    temp_df["redzone_rush_td"] = int(value["_attributes"]["tdrush"])
                except Exception:
                    temp_df["redzone_rush_td"] = 0

                try:

                    temp_df["redzone_pass_td"] = int(value["_attributes"]["tdpass"])
                except Exception:
                    temp_df["redzone_pass_td"] = 0

                try:

                    temp_df["redzone_fgm"] = int(value["_attributes"]["fgmade"])
                except Exception:
                    temp_df["redzone_fgm"] = 0

                try:

                    temp_df["redzone_end_fga"] = int(value["_attributes"]["endfga"])
                except Exception:
                    temp_df["redzone_end_fga"] = 0


                try:
                    temp_df["redzone_end_downs"] = int(value["_attributes"]["enddowns"])
                except Exception:
                    temp_df["redzone_end_downs"] = 0


                try:
                    temp_df["redzone_end_int"] = int(value["_attributes"]["endint"])
                except Exception:
                    temp_df["redzone_end_int"] = 0


                try:
                    temp_df["redzone_end_fumble"] = int(value["_attributes"]["endfumb"])
                except Exception:
                    temp_df["redzone_end_fumble"] = 0


                try:
                    temp_df["redzone_end_half"] = int(value["_attributes"]["endhalf"])
                except Exception:
                    temp_df["redzone_end_half"] = 0


                try:
                    temp_df["redzone_end_game"] = int(value["_attributes"]["endgame"])
                except Exception:
                    temp_df["redzone_end_game"] = 0


            elif key == "rush":
                if value == {}:
                    continue
                temp_df["rush_att"] = int(value["_attributes"]["att"])
                temp_df["rush_yds"] = int(value["_attributes"]["yds"])

                try:
                    temp_df["rush_yds_gain"] = int(value["_attributes"]["gain"])
                except Exception:
                    temp_df["rush_yds_gain"] = np.nan
                    logging.info(
                        f"No rush yards gain data found for {team_name} in `{game_id}`."
                    )

                try:
                    if value["_attributes"]["loss"] == "":
                        value["_attributes"]["loss"] = 0
                    temp_df["rush_yds_loss"] = int(value["_attributes"]["loss"])
                except Exception:
                    temp_df["rush_yds_loss"] = np.nan
                    logging.info(
                        f"No rush yards loss data found for {team_name} in `{game_id}`."
                    )

                temp_df["rush_td"] = int(value["_attributes"]["td"])
                try:
                    temp_df["rush_long"] = int(value["_attributes"]["long"])
                except Exception:
                    temp_df["rush_long"] = np.nan
                    logging.info(
                        f"No rush long data found for {team_name} in `{game_id}`."
                    )

            elif key == "pass":
                if value == {}:
                    continue
                temp_df["pass_comp"] = int(value["_attributes"]["comp"])
                temp_df["pass_att"] = int(value["_attributes"]["att"])
                temp_df["pass_yds"] = int(value["_attributes"]["yds"])
                temp_df["pass_td"] = int(value["_attributes"]["td"])
                temp_df["pass_int"] = int(value["_attributes"]["int"])
                try:
                    temp_df["pass_long"] = int(value["_attributes"]["long"])
                except Exception:
                    temp_df["pass_long"] = np.nan
                    logging.info(
                        f"No pass long data found for {team_name} in `{game_id}`."
                    )
            elif key == "punt":
                if value == {}:
                    continue
                temp_df["punt_att"] = int(value["_attributes"]["no"])
                temp_df["punt_gross_yds"] = int(value["_attributes"]["yds"])
                temp_df["punt_long"] = int(value["_attributes"]["long"])
                temp_df["punt_blk"] = int(value["_attributes"]["blkd"])
                temp_df["punt_tb"] = int(value["_attributes"]["tb"])
                temp_df["punt_fc"] = int(value["_attributes"]["fc"])
                temp_df["punt_50+"] = int(value["_attributes"]["plus50"])
                temp_df["punt_in_20"] = int(value["_attributes"]["inside20"])
                temp_df["punt_gross_avg"] = (
                    temp_df["punt_gross_yds"] / temp_df["punt_att"]
                )
                temp_df["punt_gross_avg"] = temp_df["punt_gross_avg"].round(3)
            elif key == "ko":
                if value == {}:
                    continue
                temp_df["kickoff_att"] = int(value["_attributes"]["no"])
                temp_df["kickoff_yds"] = int(value["_attributes"]["yds"])
                temp_df["kickoff_out_of_bounds"] = int(value["_attributes"]["ob"])
                temp_df["kickoff_tb"] = int(value["_attributes"]["tb"])
            elif key == "pat":
                if value == {}:
                    continue
                try:
                    temp_df["kick_xpm"] = int(value["_attributes"]["kickmade"])
                except Exception:
                    temp_df["kick_xpm"] = 0
                    logging.info(f"No XPM data found for {team_name} in `{game_id}`.")

                try:
                    temp_df["kick_xpa"] = int(value["_attributes"]["kickatt"])
                except Exception:
                    temp_df["kick_xpa"] = 0
                    logging.info(f"No XPM data found for {team_name} in `{game_id}`.")

                try:
                    temp_df["2PM_pass_att"] = int(value["_attributes"]["passatt"])
                except Exception:
                    temp_df["2PM_pass_att"] = 0
                    logging.info(f"No 2PA data found for {team_name} in `{game_id}`.")
                try:
                    temp_df["2PM_pass_made"] = int(value["_attributes"]["passmade"])
                except Exception:
                    temp_df["2PM_pass_made"] = 0
                    logging.info(f"No 2PT data found for {team_name} in `{game_id}`.")
                if temp_df["kick_xpa"].iloc[0] != 0:
                    temp_df["kick_xp%"] = temp_df["kick_xpm"] / temp_df["kick_xpa"]
                    temp_df["kick_xp%"] = temp_df["kick_xp%"].round(3)
            elif key == "defense":
                if value == {}:
                    continue
                try:
                    temp_df["defense_tackles_total"] = int(value["_attributes"]["tot_tack"])
                except Exception:
                    logging.info(
                        f"No TOTAL tackle data found for {team_name} in `{game_id}`."
                    )

                try:
                    temp_df["defense_tackles_solo"] = int(value["_attributes"]["tackua"])
                except Exception:
                    logging.info(
                        f"No SOLO tackle data found for {team_name} in `{game_id}`."
                    )

                try:
                    temp_df["defense_tackles_ast"] = int(value["_attributes"]["tacka"])
                except Exception:
                    logging.info(
                        f"No AST tackle data found for {team_name} in `{game_id}`."
                    )

                try:
                    temp_df["defense_tfl_solo"] = int(value["_attributes"]["tflua"])
                except Exception:
                    temp_df["defense_tfl_solo"] = np.nan
                    logging.info(
                        f"No SOLO TFL data found for {team_name} in `{game_id}`."
                    )

                try:
                    temp_df["defense_tfl_ast"] = int(value["_attributes"]["tfla"])
                except Exception:
                    temp_df["defense_tfl_ast"] = np.nan
                    logging.info(
                        f"No AST TFL data found for {team_name} in `{game_id}`."
                    )

                try:
                    temp_df["defense_tfl"] = temp_df["defense_tfl_solo"] + (
                        temp_df["defense_tfl_ast"] / 2
                    )
                    temp_df["defense_tfl"] = temp_df["defense_tfl"].round(1)
                except Exception:
                    temp_df["defense_tfl"] = np.nan
                    logging.info(f"No TFL data found for {team_name} in `{game_id}`.")

                try:
                    temp_df["defense_tfl_YDS"] = int(value["_attributes"]["tflyds"])
                except Exception:
                    temp_df["defense_tfl_YDS"] = np.nan
                    logging.info(
                        f"No TFL yds data found for {team_name} in `{game_id}`."
                    )

                try:
                    temp_df["defense_sacks"] = int(value["_attributes"]["sacks"])
                except Exception:
                    temp_df["defense_sacks"] = np.nan
                    logging.info(
                        f"No sack data found for {team_name} in `{game_id}`."
                    )
                try:
                    temp_df["defense_sack_yds"] = int(value["_attributes"]["sacks"])
                except Exception:
                    temp_df["defense_sack_yds"] = np.nan
                    logging.info(
                        f"No sack data found for {team_name} in `{game_id}`."
                    )

                try:
                    temp_df["defense_pbu"] = int(value["_attributes"]["brup"])
                except Exception:
                    temp_df["defense_pbu"] = np.nan
                    logging.info(f"No PBU data found for {team_name} in `{game_id}`.")

            elif key == "kr":
                if value == {}:
                    continue
                temp_df["kick_return_num"] = int(value["_attributes"]["no"])
                temp_df["kick_return_yds"] = int(value["_attributes"]["yds"])
                temp_df["kick_return_td"] = int(value["_attributes"]["td"])
                temp_df["kick_return_long"] = int(value["_attributes"]["long"])
            elif key == "pr":
                if value == {}:
                    continue
                temp_df["punt_return_num"] = int(value["_attributes"]["no"])
                temp_df["punt_return_yds"] = int(value["_attributes"]["yds"])
                temp_df["punt_return_td"] = int(value["_attributes"]["td"])
                temp_df["punt_return_long"] = int(value["_attributes"]["long"])
            elif key == "ir":
                if value == {}:
                    continue
                temp_df["defense_interceptions_num"] = int(value["_attributes"]["no"])
                temp_df["defense_interceptions_yds"] = int(value["_attributes"]["yds"])
                temp_df["defense_interceptions_td"] = int(value["_attributes"]["td"])
                temp_df["defense_interceptions_long"] = int(
                    value["_attributes"]["long"]
                )
            elif key == "fg":
                if value == {}:
                    continue
                temp_df["kick_fgm"] = int(value["_attributes"]["made"])
                temp_df["kick_fga"] = int(value["_attributes"]["att"])
                temp_df["kick_fg%"] = temp_df["kick_fgm"] / temp_df["kick_fga"]
                temp_df["kick_fg%"] = temp_df["kick_fg%"].round(3)
                temp_df["kick_fg_long"] = int(value["_attributes"]["long"])
                temp_df["kick_fg_blk"] = int(value["_attributes"]["blkd"])
            elif key == "fr":
                if value == {}:
                    continue
                temp_df["defense_fr"] = int(value["_attributes"]["no"])
                temp_df["defense_fr_yds"] = int(value["_attributes"]["yds"])
                temp_df["defense_fr_td"] = int(value["_attributes"]["td"])
                temp_df["defense_fr_long"] = int(value["_attributes"]["long"])
            elif key == "fgr":
                temp_df["field_goal_return_num"] = int(value["_attributes"]["no"])
                temp_df["field_goal_return_yds"] = int(value["_attributes"]["yds"])
                try:
                    temp_df["field_goal_return_td"] = int(value["_attributes"]["td"])
                except Exception:
                    temp_df["field_goal_return_td"] = 0
                    logging.info(
                        f"No FG return TD data found for {team_name} in `{game_id}`."
                    )
            elif key == "player":
                # handled in `parse_elf_player_stats()`
                pass
            elif key == "scoring":
                # data here is redundant
                pass
            elif key == "rcv":
                # data here is redundant
                pass
            else:
                raise KeyError(f"Unhandled key `{key}`.")
        data_df_arr.append(temp_df)
        del temp_df

    data_df = pd.concat(data_df_arr, ignore_index=True)
    data_df = data_df.reindex(columns=stat_columns)
    return data_df


def parse_raw_elf_pbp(json_data: dict) -> pd.DataFrame:
    """
    """
    data_df_arr = []
    data_df = pd.DataFrame()

    json_data = json_data["fbgame"]
    game_id = json_data["venue"]["_attributes"]["gameid"]
    game_date = json_data["venue"]["_attributes"]["date"]

    game_date += "T" + json_data["venue"]["_attributes"]["start"]
    game_date = game_date.replace(">", ":")
    game_date = game_date.replace("T19H", "T19:00")
    game_date = game_date.replace("T19h", "T19:00")
    game_date = game_date.replace("T18.00", "T18:00")

    game_location = json_data["venue"]["_attributes"]["location"]
    game_stadium = json_data["venue"]["_attributes"]["stadium"]

    away_abv = json_data["venue"]["_attributes"]["visid"]
    home_abv = json_data["venue"]["_attributes"]["homeid"]
    away_name = json_data["venue"]["_attributes"]["visname"]
    home_name = json_data["venue"]["_attributes"]["homename"]


def main():
    json_list = get_json_in_folder("raw_game_data/json")

    team_data_df = pd.DataFrame()
    team_data_df_arr = []

    player_data_df = pd.DataFrame()
    player_data_df_arr = []

    for json_file in tqdm(json_list):

        json_str = ""
        with open(json_file, "r") as f:
            json_str = f.read()

        json_data = json.loads(json_str)

        temp_df = parse_elf_team_stats(json_data=json_data)
        team_data_df_arr.append(temp_df)

        del temp_df

        temp_df = parse_elf_player_stats(json_data=json_data)
        player_data_df_arr.append(temp_df)

        del temp_df

    team_data_df = pd.concat(team_data_df_arr, ignore_index=True)
    team_data_df.to_csv("game_stats/team/elf_team_stats.csv", index=False)
    del team_data_df_arr

    player_data_df = pd.concat(player_data_df_arr, ignore_index=True)
    season_arr = player_data_df["season"].to_list()
    season_arr = set(season_arr)
    for s in season_arr:
        try:
            s = int(s)
        except ValueError:
            s = 2021
        temp_df = player_data_df[player_data_df["season"] == s]
        temp_df.to_csv(
            f"game_stats/player/{s}_elf_player_stats.csv",
            index=False
        )
        del temp_df

    del player_data_df_arr


if __name__ == "__main__":
    main()

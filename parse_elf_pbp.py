import json
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# from elf_utils import get_csv_in_folder, get_json_in_folder
from get_elf_schedule import get_elf_schedule


def get_elf_game_pbp_json(game_id: str):
    """

    """
    # with open(json_filepath, 'r') as f:
    #     json_string = f.read()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = f"https://europeanleague.football/game-center/schedule/{game_id}"
    print(f'\nGetting PBP data from game ID {game_id}.')
    response = requests.get(url, headers=headers)
    web_data = BeautifulSoup(response.text, features='lxml')
    del response
    print(f'Parsing PBP data from game ID {game_id}')
    quarters_data = web_data.find_all(
        'div', {'class': '@container flex flex-col gap-12'})

    with open('test.html', 'w+', encoding='utf-8') as f:
        f.write(str(web_data))
    for i in quarters_data:
        print(i.text)

    # Data Variable declarations
    ##################################################################################
    play_id = 0
    # game_id = ""
    home_team = ""
    away_team = ""
    season_type = "REG"
    week = 0
    posteam = ""
    posteam = ""
    defteam = ""
    side_of_field = ""
    yardline_100 = 0
    game_date = 0
    quarter_seconds_remaining = 0
    half_seconds_remaining = 0
    game_seconds_remaining = 0
    game_half = ""  # "Half1", "Half2", or "Overtime"
    quarter_end = 0  # 0/1 Boolean
    drive = 0  # Drive Number.
    sp = 0  # 0/1 Boolean, indicates scoring play
    qtr = 0  # Quarter (OT = 5+)
    down = 0

    goal_to_go = 0  # 0/1 Boolean, indicates if the down is a
    # "1st and goal", "2nd and goal", "3rd and goal",
    # or "4th and goal" situation.

    time = ""  # MM:SS time of the player
    yrdln = ""  # TM99 format
    ydstogo = 0  # Yards to gain a 1st down.
    ydsnet = 0  # Net yards gained/lost this drive.
    desc = ""  # Play description.
    play_type = ""
    yards_gained = 0  # Yards gained/lost on this specific play.
    shotgun = 0  # 0/1 Boolean, indicates if offense is in shotgun.
    no_huddle = 0  # 0/1 Boolean, indicates if offense is in hurry-up mode.

    qb_dropback = 0  # Indicates if this play started out as a passing play.
    # This is NULL if it's a play that is called off due to penalty.

    qb_kneel = 0  # 0/1 Boolean
    qb_spike = 0  # 0/1 Boolean
    qb_scramble = 0  # 0/1 Boolean

    # Indicates if this is a "short" pass (<10), or a "deep" pass (>10).
    pass_length = ""

    # Indicates pass location ("left", "right", or "middle")
    pass_location = ""

    # Indicates the air yardage of the throw (if this is a pass play)
    air_yards = 0

    yards_after_catch = 0  # If possible,
    # indicates how many yards were gained/lost after the catch.

    run_location = ""  # Indicates run direction ("left", "right", or "middle")

    run_gap = ""  # Further indicates run direction by the specific gap.
    # This can be the A-gap ("middle"), B-gap ("guard"), or the C-gap ("end").

    field_goal_result = ""  # If this is a FG attempt play, this indicates
    # if the kick was "made", "missed", or "blocked".

    kick_distance = 0  # On a kickoff/punt/FG, this is the actual distance of the FG,
    # or how long the punt/kickoff was.

    two_point_conv_result = ""  # On a 2PC, this indicates if the play was a
    # "success" or "failure"

    home_timeouts_remaining = 3
    away_timeouts_remaining = 3

    timeout = 0  # 0/1 Boolean
    timeout_team = ""  # Indicates the team who took the timeout
    td_team = ""
    td_player_name = ""
    td_player_id = ""

    posteam_timeouts_remaining = 0
    defteam_timeouts_remaining = 0
    total_home_score = 0
    total_away_score = 0
    posteam_score = 0
    defteam_score = 0

    score_differential = 0  # Score diff.
    # Positive = offense leading, Negative = defense leading.

    # If a score happens, these 2 variables will be greater
    # than `total_home_score` and `total_away_score`.
    posteam_score_post = 0
    defteam_score_post = 0

    score_differential_post = 0

    punt_blocked = 0  # 0/1 Boolean
    first_down_rush = 0  # 0/1 Boolean
    first_down_pass = 0  # 0/1 Boolean
    first_down_penalty = 0  # 0/1 Boolean
    third_down_converted = 0  # 0/1 Boolean
    third_down_failed = 0  # 0/1 Boolean
    fourth_down_converted = 0  # 0/1 Boolean
    fourth_down_failed = 0  # 0/1 Boolean
    incomplete_pass = 0  # 0/1 Boolean
    touchback = 0  # 0/1 Boolean
    interception = 0  # 0/1 Boolean
    punt_inside_twenty = 0  # 0/1 Boolean
    punt_in_endzone = 0  # 0/1 Boolean
    punt_out_of_bounds = 0  # 0/1 Boolean
    punt_downed = 0  # 0/1 Boolean
    punt_fair_catch = 0  # 0/1 Boolean
    kickoff_inside_twenty = 0  # 0/1 Boolean
    kickoff_in_endzone = 0  # 0/1 Boolean
    kickoff_out_of_bounds = 0  # 0/1 Boolean
    kickoff_downed = 0  # 0/1 Boolean
    kickoff_fair_catch = 0  # 0/1 Boolean
    fumble_forced = 0  # 0/1 Boolean
    fumble_not_forced = 0  # 0/1 Boolean
    fumble_out_of_bounds = 0  # 0/1 Boolean
    solo_tackle = 0  # 0/1 Boolean
    safety = 0  # 0/1 Boolean
    penalty = 0  # 0/1 Boolean
    tackled_for_loss = 0  # 0/1 Boolean
    own_kickoff_recovery = 0  # 0/1 Boolean
    own_kickoff_recovery_td = 0  # 0/1 Boolean
    qb_hit = 0  # 0/1 Boolean
    rush_attempt = 0  # 0/1 Boolean
    pass_attempt = 0  # 0/1 Boolean
    sack = 0  # 0/1 Boolean
    touchdown = 0  # 0/1 Boolean
    pass_touchdown = 0  # 0/1 Boolean
    rush_touchdown = 0  # 0/1 Boolean
    return_touchdown = 0  # 0/1 Boolean
    extra_point_attempt = 0  # 0/1 Boolean
    two_point_attempt = 0  # 0/1 Boolean
    field_goal_attempt = 0  # 0/1 Boolean
    kickoff_attempt = 0  # 0/1 Boolean
    punt_attempt = 0  # 0/1 Boolean
    fumble = 0  # 0/1 Boolean
    complete_pass = 0  # 0/1 Boolean
    assist_tackle = 0  # 0/1 Boolean
    lateral_reception = 0  # 0/1 Boolean
    lateral_rush = 0  # 0/1 Boolean
    lateral_return = 0  # 0/1 Boolean
    lateral_recovery = 0  # 0/1 Boolean

    passer_player_id = ""
    passer_player_name = ""
    passing_yards = 0

    receiver_player_id = ""
    receiver_player_name = ""
    receiving_yards = 0

    rusher_player_id = ""
    rusher_player_name = ""
    rushing_yards = ""

    lateral_receiver_player_id = ""
    lateral_receiver_player_name = ""
    lateral_receiving_yards = 0

    lateral_rusher_player_id = ""
    lateral_rusher_player_name = ""
    lateral_rushing_yards = 0

    lateral_sack_player_id = ""
    lateral_sack_player_name = ""

    interception_player_id = ""
    interception_player_name = ""

    lateral_interception_player_id = ""
    lateral_interception_player_name = ""

    punt_returner_player_id = ""
    punt_returner_player_name = ""

    lateral_punt_returner_player_id = ""
    lateral_punt_returner_player_name = ""

    kickoff_returner_player_name = ""
    kickoff_returner_player_id = ""

    lateral_kickoff_returner_player_id = ""
    lateral_kickoff_returner_player_name = ""

    punter_player_id = ""
    punter_player_name = ""

    kicker_player_id = ""
    kicker_player_name = ""

    own_kickoff_recovery_player_id = ""
    own_kickoff_recovery_player_name = ""

    blocked_player_id = ""
    blocked_player_name = ""

    tackle_for_loss_1_player_id = ""
    tackle_for_loss_1_player_name = ""

    tackle_for_loss_2_player_id = ""
    tackle_for_loss_2_player_name = ""

    qb_hit_2_player_id = ""
    qb_hit_2_player_name = ""

    forced_fumble_player_1_team = ""
    forced_fumble_player_1_player_id = ""
    forced_fumble_player_1_player_name = ""

    forced_fumble_player_2_team = ""
    forced_fumble_player_2_player_id = ""
    forced_fumble_player_2_player_name = ""

    solo_tackle_1_team = ""
    solo_tackle_1_player_id = ""
    solo_tackle_1_player_name = ""

    solo_tackle_2_team = ""
    solo_tackle_2_player_id = ""
    solo_tackle_2_player_name = ""

    assist_tackle_1_team = ""
    assist_tackle_1_player_id = ""
    assist_tackle_1_player_name = ""

    assist_tackle_2_team = ""
    assist_tackle_2_player_id = ""
    assist_tackle_2_player_name = ""

    assist_tackle_3_team = ""
    assist_tackle_3_player_id = ""
    assist_tackle_3_player_name = ""

    assist_tackle_4_team = ""
    assist_tackle_4_player_id = ""
    assist_tackle_4_player_name = ""

    tackle_with_assist = 0  # 0/1 Boolean

    pass_defense_1_player_id = ""
    pass_defense_1_player_name = ""

    pass_defense_2_player_id = ""
    pass_defense_2_player_name = ""

    fumbled_1_team = ""
    fumbled_1_player_id = ""
    fumbled_1_player_name = ""

    fumbled_2_team = ""
    fumbled_2_player_id = ""
    fumbled_2_player_name = ""

    fumble_recovery_1_team = ""
    fumble_recovery_1_player_id = ""
    fumble_recovery_1_yards = ""
    fumble_recovery_1_player_name = ""

    fumble_recovery_2_team = ""
    fumble_recovery_2_player_id = ""
    fumble_recovery_2_yards = ""
    fumble_recovery_2_player_name = ""

    sack_player_id = ""
    sack_player_name = ""

    half_sack_1_player_id = ""
    half_sack_1_player_name = ""

    half_sack_2_player_id = ""
    half_sack_2_player_name = ""

    return_team = ""
    return_yards = ""

    penalty_team = ""
    penalty_player_id = ""
    penalty_player_name = ""
    penalty_yards = 0
    penalty_type = ""

    replay_or_challenge = 0  # 0/1 Boolean
    replay_or_challenge_result = ""  # Can be "denied", "upheld", or "reversed"

    defensive_two_point_attempt = 0  # 0/1 Boolean
    defensive_two_point_conv = 0  # 0/1 Boolean
    defensive_extra_point_attempt = 0  # 0/1 Boolean
    defensive_extra_point_conv = 0  # 0/1 Boolean

    safety_player_id = ""
    safety_player_name = ""

    season = 0

    # Increases by 1 if there is a 1st down, or a change of possession.
    series = 0

    series_success = 0  # 0/1 Boolean
    series_result = ""

    # Irrelivant for our purposes, but in the nflverse PBP format.
    order_sequence = None

    start_time = ""  # kickoff time of the game, in EST
    time_of_day = ""  # UTC time of the play
    stadium = ""  # Stadium name
    weather = ""
    play_clock = 0  # Play clock when the ball was snapped.

    # 0/1 Boolean indicating that the play was deleted from existance.
    play_deleted = 0

    # 0/1 Boolean indicating that the play was a ST play.
    special_teams_play = 0


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

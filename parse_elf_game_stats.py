
import json
from datetime import datetime

import numpy as np
import pandas as pd
from tqdm import tqdm

from elf_utils import get_json_in_folder


def check_elf_stats(save=False):
    """

    """
    json_file_list = get_json_in_folder()
    participation_df = pd.DataFrame()
    row_df = pd.DataFrame()

    # print(json_file_list)

    for json_file in tqdm(json_file_list):
        with open(json_file, 'r') as f:
            json_string = f.read()

        # print(f'\n{json_file}')
        json_data = json.loads(json_string)

        game_id = json_data['venue']['_attributes']['gameid']

        game_date = str(json_data['venue']['_attributes']['date'])
        game_date = datetime.strptime(game_date, '%m/%d/%Y')
        game_season = game_date.year

        home_id = json_data['venue']['_attributes']['homeid']
        home_name = json_data['venue']['_attributes']['homename']

        visitor_id = json_data['venue']['_attributes']['visid']
        visitor_name = json_data['venue']['_attributes']['visname']

        for i in json_data['visitor_players']:
            # print(i['_attributes']['name'])
            row_df = pd.DataFrame(
                {
                    'season': game_season,
                    'game_id': game_id,
                    'team_id': visitor_id,
                    'team_name': visitor_name,
                    'loc': 'A',
                    'opponent_id': home_id,
                    'opponent_name': home_name

                },
                index=[0]
            )

            if str(i['_attributes']['name']).lower() != 'team' and str(i['_attributes']['name']).lower() != 'tm':
                player_uni = i['_attributes']['uni']
                player_name = i['_attributes']['name']
                player_short_name = i['_attributes']['shortname']
                player_check_name = i['_attributes']['checkname']
                player_GP = i['_attributes']['gp']

                try:
                    player_GS = int(i['_attributes']['gs'])
                except:
                    player_GS = 0

                try:
                    player_pos = i['_attributes']['opos']
                except:
                    try:
                        player_pos = i['_attributes']['dpos']
                    except:
                        player_pos = None

                for (key, value) in i.items():
                    if key == "_attributes":
                        pass
                    elif key == "pass":  # Passing Stats
                        for j in value['_attributes']:
                            if j == "comp":
                                pass
                            elif j == "att":
                                pass
                            elif j == "int":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            elif j == "sacks":
                                pass
                            elif j == "sackyds":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "rush":  # Rushing Stats
                        for j in value['_attributes']:
                            if j == "att":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "gain":
                                pass
                            elif j == "loss":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "rcv":  # Receiving Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "fumbles":  # Receiving Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "lost":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "scoring":  # General Scoring
                        for j in value['_attributes']:
                            if j == "td":
                                pass
                            elif j == "fg":
                                pass
                            elif j == "saf":
                                pass
                            elif j == "patrush":
                                pass
                            elif j == "patrcv":
                                pass
                            elif j == "patkick":
                                pass
                            elif j == "patretkick":
                                # Blocked XP, returned for 2 pts by defense.
                                pass
                            elif j == "patretfumb":
                                # Fumble on XP/2PC, returned for 2 pts by defense.
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "defense":  # General Defense
                        # (tackles, sacks, fumble recoveries)
                        for j in value['_attributes']:
                            if j == "tackua":  # Solo Tackles
                                pass
                            elif j == "tacka":  # Ast. Tackles
                                pass
                            elif j == "tot_tack":  # Total Tackles
                                pass
                            elif j == "tflua":  # solo TFL
                                pass
                            elif j == "tfla":  # Ast. TFL
                                pass
                            elif j == "tflyds":  # TFL Yds.
                                pass
                            elif j == "sacks":  # Sacks
                                pass
                            elif j == "sackua":  # Solo Sacks
                                pass
                            elif j == "sacka":  # Ast. Sacks
                                pass
                            elif j == "sackyds":  # Sack Yds.
                                pass
                            elif j == "brup":  # PBUs
                                pass
                            elif j == "int":  # Interceptions
                                pass
                            elif j == "intyds":  # INT Yds.
                                pass
                            elif j == "ff":  # forced fumbles
                                pass
                            elif j == "fr":  # fumble recoveries
                                pass
                            elif j == "fryds":  # FR Yds.
                                pass
                            elif j == "blkd":  # Blocked Kicks
                                pass
                            elif j == "qbh":  # QB Hits
                                pass
                            elif j == "saf":  # Safties recorded
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "ir":  # Interception Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "fr":  # Interception Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "fg":  # Field Goal Stats
                        for j in value['_attributes']:
                            if j == "made":
                                pass
                            elif j == "att":
                                pass
                            elif j == "long":
                                pass
                            elif j == "blkd":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "pat":  # Extra Points
                        for j in value['_attributes']:
                            if j == "kickmade":
                                pass
                            elif j == "kickatt":
                                pass
                            elif j == "blkd":
                                pass
                            elif j == "retkmade":
                                pass
                            elif j == "retkatt":
                                pass
                            elif j == "retfatt":
                                pass
                            elif j == "retfmade":
                                pass
                            elif j == "passatt":
                                pass
                            elif j == "passmade":
                                pass
                            elif j == "rushatt":
                                pass
                            elif j == "rushmade":
                                pass
                            elif j == "rcvatt":
                                pass
                            elif j == "rcvmade":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "ko":  # Kickoff Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "ob":
                                pass
                            elif j == "tb":
                                pass
                            elif j == "fcyds":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "punt":  # Punting Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "long":
                                pass
                            elif j == "blkd":
                                pass
                            elif j == "tb":
                                pass
                            elif j == "fc":
                                pass
                            elif j == "plus50":
                                pass
                            elif j == "inside20":
                                pass
                            elif j == "avg":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "pr":  # Kick Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "kr":  # Kick Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)
                    elif key == "fgr":  # Missed FG Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)
                    else:
                        raise ValueError(f'Unhandled Data Key:\n{key}')

        for i in json_data['visitor_players']:
            player_uni = i['_attributes']['uni']
            player_name = i['_attributes']['name']
            player_short_name = i['_attributes']['shortname']
            player_check_name = i['_attributes']['checkname']
            player_GP = i['_attributes']['gp']

            try:
                player_GS = int(i['_attributes']['gs'])
            except:
                player_GS = 0

            try:
                player_pos = i['_attributes']['opos']
            except:
                try:
                    player_pos = i['_attributes']['dpos']
                except:
                    player_pos = None

                for (key, value) in i.items():
                    if key == "_attributes":
                        pass
                    elif key == "pass":  # Passing Stats
                        for j in value['_attributes']:
                            if j == "comp":
                                pass
                            elif j == "att":
                                pass
                            elif j == "int":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            elif j == "sacks":
                                pass
                            elif j == "sackyds":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "rush":  # Rushing Stats
                        for j in value['_attributes']:
                            if j == "att":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "gain":
                                pass
                            elif j == "loss":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "rcv":  # Receiving Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "fumbles":  # Receiving Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "lost":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "scoring":  # General Scoring
                        for j in value['_attributes']:
                            if j == "td":
                                pass
                            elif j == "fg":
                                pass
                            elif j == "saf":
                                pass
                            elif j == "patrush":
                                pass
                            elif j == "patrcv":
                                pass
                            elif j == "patkick":
                                pass
                            elif j == "patretkick":
                                # Blocked XP, returned for 2 pts by defense.
                                pass
                            elif j == "patretfumb":
                                # Fumble on XP/2PC, returned for 2 pts by defense.
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "defense":  # General Defense
                        # (tackles, sacks, fumble recoveries)
                        for j in value['_attributes']:
                            if j == "tackua":  # Solo Tackles
                                pass
                            elif j == "tacka":  # Ast. Tackles
                                pass
                            elif j == "tot_tack":  # Total Tackles
                                pass
                            elif j == "tflua":  # solo TFL
                                pass
                            elif j == "tfla":  # Ast. TFL
                                pass
                            elif j == "tflyds":  # TFL Yds.
                                pass
                            elif j == "sacks":  # Sacks
                                pass
                            elif j == "sackua":  # Solo Sacks
                                pass
                            elif j == "sacka":  # Ast. Sacks
                                pass
                            elif j == "sackyds":  # Sack Yds.
                                pass
                            elif j == "brup":  # PBUs
                                pass
                            elif j == "int":  # Interceptions
                                pass
                            elif j == "intyds":  # INT Yds.
                                pass
                            elif j == "ff":  # forced fumbles
                                pass
                            elif j == "fr":  # fumble recoveries
                                pass
                            elif j == "fryds":  # FR Yds.
                                pass
                            elif j == "blkd":  # Blocked Kicks
                                pass
                            elif j == "qbh":  # QB Hits
                                pass
                            elif j == "saf":  # Safties recorded
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "ir":  # Interception Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "fr":  # Interception Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "fg":  # Field Goal Stats
                        for j in value['_attributes']:
                            if j == "made":
                                pass
                            elif j == "att":
                                pass
                            elif j == "long":
                                pass
                            elif j == "blkd":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "pat":  # Extra Points
                        for j in value['_attributes']:
                            if j == "kickmade":
                                pass
                            elif j == "kickatt":
                                pass
                            elif j == "blkd":
                                pass
                            elif j == "retkmade":
                                pass
                            elif j == "retkatt":
                                pass
                            elif j == "retfatt":
                                pass
                            elif j == "retfmade":
                                pass
                            elif j == "passatt":
                                pass
                            elif j == "passmade":
                                pass
                            elif j == "rushatt":
                                pass
                            elif j == "rushmade":
                                pass
                            elif j == "rcvatt":
                                pass
                            elif j == "rcvmade":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "ko":  # Kickoff Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "ob":
                                pass
                            elif j == "tb":
                                pass
                            elif j == "fcyds":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "punt":  # Punting Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "long":
                                pass
                            elif j == "blkd":
                                pass
                            elif j == "tb":
                                pass
                            elif j == "fc":
                                pass
                            elif j == "plus50":
                                pass
                            elif j == "inside20":
                                pass
                            elif j == "avg":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "pr":  # Kick Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)

                    elif key == "kr":  # Kick Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)
                    elif key == "fgr":  # Missed FG Return Stats
                        for j in value['_attributes']:
                            if j == "no":
                                pass
                            elif j == "yds":
                                pass
                            elif j == "td":
                                pass
                            elif j == "long":
                                pass
                            else:
                                raise ValueError(j)
                    else:
                        raise ValueError(f'Unhandled Data Key:\n{key}')


def parse_elf_game_stats(save=False):
    """

    """
    json_file_list = get_json_in_folder()
    player_stats_df = pd.DataFrame()
    row_df = pd.DataFrame()

    pass_df = pd.DataFrame()
    rush_df = pd.DataFrame()
    rec_df = pd.DataFrame()
    fumbles_df = pd.DataFrame()
    defense_df = pd.DataFrame()
    interceptions_df = pd.DataFrame()
    fumble_recoveries_df = pd.DataFrame()
    field_goals_df = pd.DataFrame()
    extra_points_df = pd.DataFrame()
    kickoffs_df = pd.DataFrame()
    punts_df = pd.DataFrame()
    punt_returns_df = pd.DataFrame()
    kick_returns_df = pd.DataFrame()
    fg_returns_df = pd.DataFrame()

    # print(json_file_list)

    for json_file in tqdm(json_file_list):
        with open(json_file, 'r') as f:
            json_string = f.read()

        # print(f'\n{json_file}')
        json_data = json.loads(json_string)

        game_id = json_data['venue']['_attributes']['gameid']

        game_date = str(json_data['venue']['_attributes']['date'])
        game_date = datetime.strptime(game_date, '%m/%d/%Y')
        game_season = game_date.year

        home_id = json_data['venue']['_attributes']['homeid']
        home_name = json_data['venue']['_attributes']['homename']

        visitor_id = json_data['venue']['_attributes']['visid']
        visitor_name = json_data['venue']['_attributes']['visname']

        for i in json_data['visitor_players']:

            team_location = 'A'

            if str(i['_attributes']['name']).lower() != 'team' and str(i['_attributes']['name']).lower() != 'tm':
                player_uni = i['_attributes']['uni']
                player_name = i['_attributes']['name']
                player_short_name = i['_attributes']['shortname']
                player_check_name = i['_attributes']['checkname']
                player_GP = i['_attributes']['gp']

                try:
                    player_GS = int(i['_attributes']['gs'])
                except:
                    player_GS = 0

                try:
                    player_pos = i['_attributes']['opos']
                except:
                    try:
                        player_pos = i['_attributes']['dpos']
                    except:
                        player_pos = None

                for (key, value) in i.items():
                    if key == "_attributes":
                        pass
                    elif key == "pass":  # Passing Stats

                        pass_comp = int(value['_attributes']['comp'])
                        pass_att = int(value['_attributes']['att'])
                        pass_yds = int(value['_attributes']['yds'])
                        pass_tds = int(value['_attributes']['td'])
                        pass_int = int(value['_attributes']['int'])
                        pass_long = int(value['_attributes']['long'])
                        pass_sacks = int(value['_attributes']['sacks'])
                        pass_sacked_yds = int(value['_attributes']['sackyds'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'pass_comp': pass_comp,
                            'pass_att': pass_att,
                            'pass_yds': pass_yds,
                            'pass_tds': pass_tds,
                            'pass_int': pass_int,
                            'pass_long': pass_long,
                            'pass_sacks': pass_sacks,
                            'pass_sacked_yds': pass_sacked_yds,
                        },
                            index=[0]
                        )

                        pass_df = pd.concat(
                            [pass_df, row_df], ignore_index=True)

                        del row_df
                        del pass_comp, pass_att, \
                            pass_yds, pass_tds, \
                            pass_int, pass_long, \
                            pass_sacks, pass_sacked_yds

                    elif key == "rush":  # Rushing Stats

                        rush_att = int(value['_attributes']['att'])
                        rush_yds = int(value['_attributes']['yds'])
                        rush_yds_gained = int(value['_attributes']['gain'])
                        rush_yds_lost = int(value['_attributes']['loss'])
                        rush_td = int(value['_attributes']['td'])
                        rush_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'rush_att': rush_att,
                            'rush_yds': rush_yds,
                            'rush_yds_gained': rush_yds_gained,
                            'rush_yds_lost': rush_yds_lost,
                            'rush_td': rush_td,
                            'rush_long': rush_long
                        },
                            index=[0]
                        )

                        rush_df = pd.concat(
                            [rush_df, row_df], ignore_index=True)

                        del row_df
                        del rush_att, rush_yds, \
                            rush_yds_gained, rush_yds_lost, \
                            rush_td, rush_long

                    elif key == "rcv":  # Receiving Stats
                        rec_targets = 0
                        rec_no = int(value['_attributes']['no'])
                        rec_yds = int(value['_attributes']['yds'])
                        rec_tds = int(value['_attributes']['td'])
                        rec_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'rec_targets': rec_targets,
                            'rec_no': rec_no,
                            'rec_yds': rec_yds,
                            'rec_tds': rec_tds,
                            'rec_long': rec_long,
                        },
                            index=[0]
                        )

                        rec_df = pd.concat(
                            [rec_df, row_df], ignore_index=True)
                        del row_df
                        del rec_no, rec_yds, \
                            rec_tds, rec_long

                    elif key == "fumbles":  # Fumble Stats

                        fumbles = int(value['_attributes']['no'])
                        fumbles_lost = int(value['_attributes']['no'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'fumbles': fumbles,
                            'fumbles_lost': fumbles_lost
                        },
                            index=[0]
                        )

                        fumbles_df = pd.concat(
                            [fumbles_df, row_df], ignore_index=True)
                        del row_df
                        del fumbles, fumbles_lost

                    elif key == "scoring":  # General Scoring
                        # There's nothing under this key that isn't in another section.
                        pass

                    elif key == "defense":  # General Defense
                        try:
                            defense_solo_tackles = int(
                                value['_attributes']['tackua'])
                        except:
                            defense_solo_tackles = 0

                        try:
                            defense_ast_tackles = int(
                                value['_attributes']['tacka'])
                        except:
                            defense_ast_tackles = 0

                        try:
                            defense_total_tackles = int(
                                value['_attributes']['tot_tack'])
                        except:
                            defense_total_tackles = 0

                        try:
                            defense_solo_tfl = int(
                                value['_attributes']['tflua'])
                        except:
                            defense_solo_tfl = 0

                        try:
                            defense_ast_tfl = int(value['_attributes']['tfla'])
                        except:
                            defense_ast_tfl = 0

                        defense_tfls = round(
                            defense_solo_tfl + (defense_ast_tfl / 2), 1)

                        try:
                            defense_tfl_yds = int(
                                value['_attributes']['tflyds'])
                        except:
                            defense_tfl_yds = 0

                        try:
                            defense_solo_sack = int(
                                value['_attributes']['sackua'])
                        except:
                            defense_solo_sack = 0

                        try:
                            defense_ast_sack = int(
                                value['_attributes']['sacka'])
                        except:
                            defense_ast_sack = 0

                        defense_sacks = round(
                            defense_solo_sack + (defense_ast_sack / 2), 1)

                        try:
                            defense_qb_hits = int(value['_attributes']['qbh'])
                        except:
                            defense_qb_hits = None

                        try:
                            defense_int = int(value['_attributes']['int'])
                        except:
                            defense_int = 0

                        try:
                            defense_int_yds = int(
                                value['_attributes']['intyds'])
                        except:
                            defense_int_yds = 0

                        try:
                            defense_pbu = int(value['_attributes']['brup'])
                        except:
                            defense_pbu = 0

                        try:
                            defense_ff = int(value['_attributes']['ff'])
                        except:
                            defense_ff = 0

                        try:
                            defense_fr = int(value['_attributes']['fr'])
                        except:
                            defense_fr = 0

                        try:
                            defense_fr_yds = int(value['_attributes']['fryds'])
                        except:
                            defense_fr_yds = 0

                        try:
                            defense_saf = int(value['_attributes']['saf'])
                        except:
                            defense_saf = 0

                        try:
                            defense_blkd = int(value['_attributes']['blkd'])
                        except:
                            defense_blkd = 0

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'defense_solo_tackles': defense_solo_tackles,
                            'defense_ast_tackles': defense_ast_tackles,
                            'defense_total_tackles': defense_total_tackles,
                            'defense_solo_tfl': defense_solo_tfl,
                            'defense_ast_tfl': defense_ast_tfl,
                            'defense_tfls': defense_tfls,
                            'defense_tfl_yds': defense_tfl_yds,
                            'defense_solo_sack': defense_solo_sack,
                            'defense_ast_sack': defense_ast_sack,
                            'defense_sacks': defense_sacks,
                            'defense_qb_hits': defense_qb_hits,
                            'defense_int': defense_int,
                            'defense_int_yds': defense_int_yds,
                            'defense_pbu': defense_pbu,
                            'defense_ff': defense_ff,
                            'defense_fr': defense_fr,
                            'defense_fr_yds': defense_fr_yds,
                            'defense_saf': defense_saf,
                            'defense_blkd': defense_blkd
                        },
                            index=[0]
                        )

                        defense_df = pd.concat(
                            [defense_df, row_df], ignore_index=True)

                        del row_df
                        del defense_solo_tackles, defense_ast_tackles, \
                            defense_total_tackles, defense_solo_tfl, \
                            defense_ast_tfl, defense_tfls, \
                            defense_tfl_yds, defense_solo_sack, \
                            defense_ast_sack, defense_sacks, \
                            defense_qb_hits, defense_int, \
                            defense_int_yds, defense_pbu, \
                            defense_ff, defense_fr, \
                            defense_fr_yds, defense_saf, defense_blkd

                    elif key == "ir":  # Interception Return Stats

                        # defense_int = int(value['_attributes']['no'])
                        # defense_int_yds = int(value['_attributes']['yds'])
                        defense_int_td = int(value['_attributes']['td'])
                        defense_int_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            # 'defense_int': defense_int,
                            # 'defense_int_yds': defense_int_yds,
                            'defense_int_td': defense_int_td,
                            'defense_int_long': defense_int_long
                        },
                            index=[0]
                        )
                        interceptions_df = pd.concat(
                            [interceptions_df, row_df], ignore_index=True)

                        del row_df
                        # del defense_int, defense_int_yds, \
                        #     defense_int_td, defense_int_long
                        del defense_int_td, defense_int_long

                    elif key == "fr":  # fumble Return Stats

                        # defense_fr = int(value['_attributes']['no'])
                        # defense_fr_yds = int(value['_attributes']['yds'])
                        defense_fr_tds = int(value['_attributes']['td'])
                        defense_fr_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'defense_fr_tds': defense_fr_tds,
                            'defense_fr_long': defense_fr_long
                        },
                            index=[0]
                        )

                        fumble_recoveries_df = pd.concat(
                            [fumble_recoveries_df, row_df], ignore_index=True)
                        del row_df
                        # del defense_fr, defense_fr_yds, \
                        #     defense_fr_tds, defense_fr_long
                        del defense_fr_tds, defense_fr_long

                    elif key == "fg":  # Field Goal Stats

                        fg_made = int(value['_attributes']['made'])
                        fg_att = int(value['_attributes']['att'])
                        fg_long = int(value['_attributes']['long'])
                        fg_blkd = int(value['_attributes']['blkd'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'fg_made': fg_made,
                            'fg_att': fg_att,
                            'fg_long': fg_long,
                            'fg_blkd': fg_blkd,
                        },
                            index=[0]
                        )

                        field_goals_df = pd.concat(
                            [field_goals_df, row_df], ignore_index=True)
                        del row_df
                        del fg_made, fg_att, \
                            fg_long, fg_blkd

                    elif key == "pat":  # Extra Points
                        try:
                            xp_made = int(value['_attributes']['kickmade'])
                        except:
                            xp_made = 0

                        try:
                            xp_att = int(value['_attributes']['kickatt'])
                        except:
                            xp_att = 0

                        try:
                            xp_blkd = int(value['_attributes']['blkd'])
                        except:
                            xp_blkd = 0

                        try:
                            two_pt_pass_made = int(
                                value['_attributes']['passmade'])
                        except:
                            two_pt_pass_made = 0

                        try:
                            two_pt_pass_att = int(
                                value['_attributes']['passatt'])
                        except:
                            two_pt_pass_att = 0

                        try:
                            two_pt_rush_made = int(
                                value['_attributes']['rushmade'])
                        except:
                            two_pt_rush_made = 0

                        try:
                            two_pt_rush_att = int(
                                value['_attributes']['rushatt'])
                        except:
                            two_pt_rush_att = 0

                        try:
                            two_pt_rec_made = int(
                                value['_attributes']['rcvmade'])
                        except:
                            two_pt_rec_made = 0

                        try:
                            two_pt_rec_att = int(
                                value['_attributes']['rcvatt'])
                        except:
                            two_pt_rec_att = 0

                        try:
                            def_two_pt_fum_made = int(
                                value['_attributes']['retfmade'])
                        except:
                            def_two_pt_fum_made = 0

                        try:
                            def_two_pt_fum_att = int(
                                value['_attributes']['retfatt'])
                        except:
                            def_two_pt_fum_att = 0

                        try:
                            def_two_pt_kick_made = int(
                                value['_attributes']['retkmade'])
                        except:
                            def_two_pt_kick_made = 0

                        try:
                            def_two_pt_kick_att = int(
                                value['_attributes']['retkatt'])
                        except:
                            def_two_pt_kick_att = 0

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'xp_made': xp_made,
                            'xp_att': xp_att,

                            'xp_blkd': xp_blkd,
                            'two_pt_pass_made': two_pt_pass_made,
                            'two_pt_pass_att': two_pt_pass_att,
                            'two_pt_rush_made': two_pt_rush_made,
                            'two_pt_rush_att': two_pt_rush_att,
                            'two_pt_rec_made': two_pt_rec_made,
                            'two_pt_rec_att': two_pt_rec_att,
                            'def_two_pt_fum_made': def_two_pt_fum_made,
                            'def_two_pt_fum_att': def_two_pt_fum_att,
                            'def_two_pt_kick_made': def_two_pt_kick_made,
                            'def_two_pt_kick_att': def_two_pt_kick_att
                        },
                            index=[0]
                        )

                        extra_points_df = pd.concat(
                            [extra_points_df, row_df], ignore_index=True)

                        del row_df
                        del two_pt_pass_made, two_pt_pass_att, \
                            two_pt_rush_made, two_pt_rush_att, \
                            two_pt_rec_made, two_pt_rec_att, \
                            def_two_pt_fum_made, def_two_pt_fum_att, \
                            def_two_pt_kick_made, def_two_pt_kick_att

                    elif key == "ko":  # Kickoff Stats

                        ko_no = int(value['_attributes']['no'])
                        ko_yds = int(value['_attributes']['yds'])
                        ko_ob = int(value['_attributes']['ob'])
                        ko_tb = int(value['_attributes']['tb'])
                        # IDK what this value is for, but it exists.
                        try:
                            ko_fc_yds = int(value['_attributes']['fcyds'])
                        except:
                            ko_fc_yds = 0

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'ko_no': ko_no,
                            'ko_yds': ko_yds,
                            'ko_ob': ko_ob,
                            'ko_tb': ko_tb,
                            'ko_fc_yds': ko_fc_yds
                        },
                            index=[0]
                        )

                        kickoffs_df = pd.concat(
                            [kickoffs_df, row_df], ignore_index=True)

                        del row_df
                        del ko_no, ko_yds, \
                            ko_ob, ko_tb, ko_fc_yds

                    elif key == "punt":  # Punting Stats

                        punt_no = int(value['_attributes']['long'])
                        punt_gross_yds = int(value['_attributes']['yds'])
                        if punt_no > 0:
                            punt_gross_avg = round(punt_gross_yds / punt_no, 1)
                        else:
                            punt_gross_avg = None
                        # This isn't in the dataset (yet), but I'm adding this
                        # for future reference/expansion.
                        punt_net_yds = None
                        punt_net_avg = None
                        punt_tb = int(value['_attributes']['tb'])
                        punt_fc = int(value['_attributes']['fc'])
                        punt_50_plus = int(value['_attributes']['plus50'])
                        punt_in_20 = int(value['_attributes']['inside20'])
                        punt_long = int(value['_attributes']['long'])
                        punt_blkd = int(value['_attributes']['blkd'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'punt_no': punt_no,
                            'punt_gross_yds': punt_gross_yds,
                            'punt_gross_avg': punt_gross_avg,
                            'punt_net_yds': punt_net_yds,
                            'punt_net_avg': punt_net_avg,
                            'punt_tb': punt_tb,
                            'punt_blkd': punt_blkd,
                            'punt_fc': punt_fc,
                            'punt_50+': punt_50_plus,
                            'punt_inside_20': punt_in_20,
                            'punt_long': punt_long

                        },
                            index=[0]
                        )

                        punts_df = pd.concat(
                            [punts_df, row_df], ignore_index=True)

                        del row_df
                        del punt_no, \
                            punt_gross_yds, punt_gross_avg, \
                            punt_net_yds, punt_net_avg, \
                            punt_tb, punt_blkd, \
                            punt_fc, punt_50_plus, \
                            punt_in_20, punt_long

                    elif key == "pr":  # Punt Return Stats

                        pr_no = int(value['_attributes']['no'])
                        pr_yds = int(value['_attributes']['yds'])
                        pr_td = int(value['_attributes']['td'])
                        pr_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'pr_no': pr_no,
                            'pr_yds': pr_yds,
                            'pr_td': pr_td,
                            'pr_long': pr_long

                        },
                            index=[0]
                        )

                        punt_returns_df = pd.concat(
                            [punt_returns_df, row_df], ignore_index=True)

                        del row_df
                        del pr_no, pr_yds, \
                            pr_td, pr_long

                    elif key == "kr":  # Kick Return Stats

                        kr_no = int(value['_attributes']['no'])
                        kr_yds = int(value['_attributes']['yds'])
                        kr_td = int(value['_attributes']['td'])
                        kr_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'kr_no': kr_no,
                            'kr_yds': kr_yds,
                            'kr_td': kr_td,
                            'kr_long': kr_long,
                        },
                            index=[0]
                        )

                        kick_returns_df = pd.concat(
                            [kick_returns_df, row_df], ignore_index=True)

                        del row_df
                        del kr_no, kr_yds, \
                            kr_td, kr_long

                    elif key == "fgr":  # Missed FG Return Stats

                        fgr_no = int(value['_attributes']['no'])
                        fgr_yds = int(value['_attributes']['yds'])
                        try:
                            fgr_td = int(value['_attributes']['td'])
                        except:
                            fgr_td = 0
                        try:
                            fgr_long = int(value['_attributes']['long'])
                        except:
                            fgr_long = 0

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'fgr_no': fgr_no,
                            'fgr_yds': fgr_yds,
                            'fgr_td': fgr_td,
                            'fgr_long': fgr_long
                        },
                            index=[0]
                        )

                        fg_returns_df = pd.concat(
                            [fg_returns_df, row_df], ignore_index=True)

                        del row_df
                        del fgr_no, fgr_yds,\
                            fgr_td, fgr_long

                    else:
                        raise ValueError(f'Unhandled Data Key:\n{key}')

        for i in json_data['home_players']:
            team_location = 'H'

            if str(i['_attributes']['name']).lower() != 'team' and str(i['_attributes']['name']).lower() != 'tm':
                player_uni = i['_attributes']['uni']
                player_name = i['_attributes']['name']
                player_short_name = i['_attributes']['shortname']
                player_check_name = i['_attributes']['checkname']
                player_GP = i['_attributes']['gp']

                try:
                    player_GS = int(i['_attributes']['gs'])
                except:
                    player_GS = 0

                try:
                    player_pos = i['_attributes']['opos']
                except:
                    try:
                        player_pos = i['_attributes']['dpos']
                    except:
                        player_pos = None

                for (key, value) in i.items():
                    if key == "_attributes":
                        pass
                    elif key == "pass":  # Passing Stats

                        pass_comp = int(value['_attributes']['comp'])
                        pass_att = int(value['_attributes']['att'])
                        pass_yds = int(value['_attributes']['yds'])
                        pass_tds = int(value['_attributes']['td'])
                        pass_int = int(value['_attributes']['int'])
                        pass_long = int(value['_attributes']['long'])
                        pass_sacks = int(value['_attributes']['sacks'])
                        pass_sacked_yds = int(value['_attributes']['sackyds'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'pass_comp': pass_comp,
                            'pass_att': pass_att,
                            'pass_yds': pass_yds,
                            'pass_tds': pass_tds,
                            'pass_int': pass_int,
                            'pass_long': pass_long,
                            'pass_sacks': pass_sacks,
                            'pass_sacked_yds': pass_sacked_yds,
                        },
                            index=[0]
                        )

                        pass_df = pd.concat(
                            [pass_df, row_df], ignore_index=True)

                        del row_df
                        del pass_comp, pass_att, \
                            pass_yds, pass_tds, \
                            pass_int, pass_long, \
                            pass_sacks, pass_sacked_yds

                    elif key == "rush":  # Rushing Stats

                        rush_att = int(value['_attributes']['att'])
                        rush_yds = int(value['_attributes']['yds'])
                        rush_yds_gained = int(value['_attributes']['gain'])
                        rush_yds_lost = int(value['_attributes']['loss'])
                        rush_td = int(value['_attributes']['td'])
                        rush_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'rush_att': rush_att,
                            'rush_yds': rush_yds,
                            'rush_yds_gained': rush_yds_gained,
                            'rush_yds_lost': rush_yds_lost,
                            'rush_td': rush_td,
                            'rush_long': rush_long
                        },
                            index=[0]
                        )

                        rush_df = pd.concat(
                            [rush_df, row_df], ignore_index=True)

                        del row_df
                        del rush_att, rush_yds, \
                            rush_yds_gained, rush_yds_lost, \
                            rush_td, rush_long

                    elif key == "rcv":  # Receiving Stats
                        rec_targets = 0
                        rec_no = int(value['_attributes']['no'])
                        rec_yds = int(value['_attributes']['yds'])
                        rec_tds = int(value['_attributes']['td'])
                        rec_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'rec_targets': rec_targets,
                            'rec_no': rec_no,
                            'rec_yds': rec_yds,
                            'rec_tds': rec_tds,
                            'rec_long': rec_long,
                        },
                            index=[0]
                        )

                        rec_df = pd.concat(
                            [rec_df, row_df], ignore_index=True)
                        del row_df
                        del rec_no, rec_yds, \
                            rec_tds, rec_long

                    elif key == "fumbles":  # Fumble Stats

                        fumbles = int(value['_attributes']['no'])
                        fumbles_lost = int(value['_attributes']['no'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'fumbles': fumbles,
                            'fumbles_lost': fumbles_lost
                        },
                            index=[0]
                        )

                        fumbles_df = pd.concat(
                            [fumbles_df, row_df], ignore_index=True)
                        del row_df
                        del fumbles, fumbles_lost

                    elif key == "scoring":  # General Scoring
                        # There's nothing under this key that isn't in another section.
                        pass

                    elif key == "defense":  # General Defense
                        try:
                            defense_solo_tackles = int(
                                value['_attributes']['tackua'])
                        except:
                            defense_solo_tackles = 0

                        try:
                            defense_ast_tackles = int(
                                value['_attributes']['tacka'])
                        except:
                            defense_ast_tackles = 0

                        try:
                            defense_total_tackles = int(
                                value['_attributes']['tot_tack'])
                        except:
                            defense_total_tackles = 0

                        try:
                            defense_solo_tfl = int(
                                value['_attributes']['tflua'])
                        except:
                            defense_solo_tfl = 0

                        try:
                            defense_ast_tfl = int(value['_attributes']['tfla'])
                        except:
                            defense_ast_tfl = 0

                        defense_tfls = round(
                            defense_solo_tfl + (defense_ast_tfl / 2), 1)

                        try:
                            defense_tfl_yds = int(
                                value['_attributes']['tflyds'])
                        except:
                            defense_tfl_yds = 0

                        try:
                            defense_solo_sack = int(
                                value['_attributes']['sackua'])
                        except:
                            defense_solo_sack = 0

                        try:
                            defense_ast_sack = int(
                                value['_attributes']['sacka'])
                        except:
                            defense_ast_sack = 0

                        defense_sacks = round(
                            defense_solo_sack + (defense_ast_sack / 2), 1)

                        try:
                            defense_qb_hits = int(value['_attributes']['qbh'])
                        except:
                            defense_qb_hits = None

                        try:
                            defense_int = int(value['_attributes']['int'])
                        except:
                            defense_int = 0

                        try:
                            defense_int_yds = int(
                                value['_attributes']['intyds'])
                        except:
                            defense_int_yds = 0

                        try:
                            defense_pbu = int(value['_attributes']['brup'])
                        except:
                            defense_pbu = 0

                        try:
                            defense_ff = int(value['_attributes']['ff'])
                        except:
                            defense_ff = 0

                        try:
                            defense_fr = int(value['_attributes']['fr'])
                        except:
                            defense_fr = 0

                        try:
                            defense_fr_yds = int(value['_attributes']['fryds'])
                        except:
                            defense_fr_yds = 0

                        try:
                            defense_saf = int(value['_attributes']['saf'])
                        except:
                            defense_saf = 0

                        try:
                            defense_blkd = int(value['_attributes']['blkd'])
                        except:
                            defense_blkd = 0

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'defense_solo_tackles': defense_solo_tackles,
                            'defense_ast_tackles': defense_ast_tackles,
                            'defense_total_tackles': defense_total_tackles,
                            'defense_solo_tfl': defense_solo_tfl,
                            'defense_ast_tfl': defense_ast_tfl,
                            'defense_tfls': defense_tfls,
                            'defense_tfl_yds': defense_tfl_yds,
                            'defense_solo_sack': defense_solo_sack,
                            'defense_ast_sack': defense_ast_sack,
                            'defense_sacks': defense_sacks,
                            'defense_qb_hits': defense_qb_hits,
                            'defense_int': defense_int,
                            'defense_int_yds': defense_int_yds,
                            'defense_pbu': defense_pbu,
                            'defense_ff': defense_ff,
                            'defense_fr': defense_fr,
                            'defense_fr_yds': defense_fr_yds,
                            'defense_saf': defense_saf,
                            'defense_blkd': defense_blkd
                        },
                            index=[0]
                        )

                        defense_df = pd.concat(
                            [defense_df, row_df], ignore_index=True)

                        del row_df
                        del defense_solo_tackles, defense_ast_tackles, \
                            defense_total_tackles, defense_solo_tfl, \
                            defense_ast_tfl, defense_tfls, \
                            defense_tfl_yds, defense_solo_sack, \
                            defense_ast_sack, defense_sacks, \
                            defense_qb_hits, defense_int, \
                            defense_int_yds, defense_pbu, \
                            defense_ff, defense_fr, \
                            defense_fr_yds, defense_saf, defense_blkd

                    elif key == "ir":  # Interception Return Stats

                        # defense_int = int(value['_attributes']['no'])
                        # defense_int_yds = int(value['_attributes']['yds'])
                        defense_int_td = int(value['_attributes']['td'])
                        defense_int_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            # 'defense_int': defense_int,
                            # 'defense_int_yds': defense_int_yds,
                            'defense_int_td': defense_int_td,
                            'defense_int_long': defense_int_long
                        },
                            index=[0]
                        )
                        interceptions_df = pd.concat(
                            [interceptions_df, row_df], ignore_index=True)

                        del row_df
                        # del defense_int, defense_int_yds, \
                        #     defense_int_td, defense_int_long
                        del defense_int_td, defense_int_long

                    elif key == "fr":  # fumble Return Stats

                        # defense_fr = int(value['_attributes']['no'])
                        # defense_fr_yds = int(value['_attributes']['yds'])
                        defense_fr_tds = int(value['_attributes']['td'])
                        defense_fr_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            # 'defense_fr': defense_fr,
                            # 'defense_fr_yds': defense_fr_yds,
                            'defense_fr_tds': defense_fr_tds,
                            'defense_fr_long': defense_fr_long
                        },
                            index=[0]
                        )

                        fumble_recoveries_df = pd.concat(
                            [fumble_recoveries_df, row_df], ignore_index=True)
                        del row_df
                        # del defense_fr, defense_fr_yds, \
                        #     defense_fr_tds, defense_fr_long
                        del defense_fr_tds, defense_fr_long

                    elif key == "fg":  # Field Goal Stats

                        fg_made = int(value['_attributes']['made'])
                        fg_att = int(value['_attributes']['att'])
                        fg_long = int(value['_attributes']['long'])
                        fg_blkd = int(value['_attributes']['blkd'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'fg_made': fg_made,
                            'fg_att': fg_att,
                            'fg_long': fg_long,
                            'fg_blkd': fg_blkd,
                        },
                            index=[0]
                        )

                        field_goals_df = pd.concat(
                            [field_goals_df, row_df], ignore_index=True)
                        del row_df
                        del fg_made, fg_att, \
                            fg_long, fg_blkd

                    elif key == "pat":  # Extra Points
                        try:
                            xp_made = int(value['_attributes']['kickmade'])
                        except:
                            xp_made = 0

                        try:
                            xp_att = int(value['_attributes']['kickatt'])
                        except:
                            xp_att = 0

                        try:
                            xp_blkd = int(value['_attributes']['blkd'])
                        except:
                            xp_blkd = 0

                        try:
                            two_pt_pass_made = int(
                                value['_attributes']['passmade'])
                        except:
                            two_pt_pass_made = 0

                        try:
                            two_pt_pass_att = int(
                                value['_attributes']['passatt'])
                        except:
                            two_pt_pass_att = 0

                        try:
                            two_pt_rush_made = int(
                                value['_attributes']['rushmade'])
                        except:
                            two_pt_rush_made = 0

                        try:
                            two_pt_rush_att = int(
                                value['_attributes']['rushatt'])
                        except:
                            two_pt_rush_att = 0

                        try:
                            two_pt_rec_made = int(
                                value['_attributes']['rcvmade'])
                        except:
                            two_pt_rec_made = 0

                        try:
                            two_pt_rec_att = int(
                                value['_attributes']['rcvatt'])
                        except:
                            two_pt_rec_att = 0

                        try:
                            def_two_pt_fum_made = int(
                                value['_attributes']['retfmade'])
                        except:
                            def_two_pt_fum_made = 0

                        try:
                            def_two_pt_fum_att = int(
                                value['_attributes']['retfatt'])
                        except:
                            def_two_pt_fum_att = 0

                        try:
                            def_two_pt_kick_made = int(
                                value['_attributes']['retkmade'])
                        except:
                            def_two_pt_kick_made = 0

                        try:
                            def_two_pt_kick_att = int(
                                value['_attributes']['retkatt'])
                        except:
                            def_two_pt_kick_att = 0

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'xp_made': xp_made,
                            'xp_att': xp_att,

                            'xp_blkd': xp_blkd,
                            'two_pt_pass_made': two_pt_pass_made,
                            'two_pt_pass_att': two_pt_pass_att,
                            'two_pt_rush_made': two_pt_rush_made,
                            'two_pt_rush_att': two_pt_rush_att,
                            'two_pt_rec_made': two_pt_rec_made,
                            'two_pt_rec_att': two_pt_rec_att,
                            'def_two_pt_fum_made': def_two_pt_fum_made,
                            'def_two_pt_fum_att': def_two_pt_fum_att,
                            'def_two_pt_kick_made': def_two_pt_kick_made,
                            'def_two_pt_kick_att': def_two_pt_kick_att
                        },
                            index=[0]
                        )

                        extra_points_df = pd.concat(
                            [extra_points_df, row_df], ignore_index=True)

                        del row_df
                        del two_pt_pass_made, two_pt_pass_att, \
                            two_pt_rush_made, two_pt_rush_att, \
                            two_pt_rec_made, two_pt_rec_att, \
                            def_two_pt_fum_made, def_two_pt_fum_att, \
                            def_two_pt_kick_made, def_two_pt_kick_att

                    elif key == "ko":  # Kickoff Stats

                        ko_no = int(value['_attributes']['no'])
                        ko_yds = int(value['_attributes']['yds'])
                        ko_ob = int(value['_attributes']['ob'])
                        ko_tb = int(value['_attributes']['tb'])
                        # IDK what this value is for, but it exists.
                        try:
                            ko_fc_yds = int(value['_attributes']['fcyds'])
                        except:
                            ko_fc_yds = 0

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'ko_no': ko_no,
                            'ko_yds': ko_yds,
                            'ko_ob': ko_ob,
                            'ko_tb': ko_tb,
                            'ko_fc_yds': ko_fc_yds
                        },
                            index=[0]
                        )

                        kickoffs_df = pd.concat(
                            [kickoffs_df, row_df], ignore_index=True)

                        del row_df
                        del ko_no, ko_yds, \
                            ko_ob, ko_tb, ko_fc_yds

                    elif key == "punt":  # Punting Stats

                        punt_no = int(value['_attributes']['long'])
                        punt_gross_yds = int(value['_attributes']['yds'])
                        if punt_no > 0:
                            punt_gross_avg = round(punt_gross_yds / punt_no, 1)
                        else:
                            punt_gross_avg = None
                        # This isn't in the dataset (yet), but I'm adding this
                        # for future reference/expansion.
                        punt_net_yds = None
                        punt_net_avg = None
                        punt_tb = int(value['_attributes']['tb'])
                        punt_fc = int(value['_attributes']['fc'])
                        punt_50_plus = int(value['_attributes']['plus50'])
                        punt_in_20 = int(value['_attributes']['inside20'])
                        punt_long = int(value['_attributes']['long'])
                        punt_blkd = int(value['_attributes']['blkd'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'punt_no': punt_no,
                            'punt_gross_yds': punt_gross_yds,
                            'punt_gross_avg': punt_gross_avg,
                            'punt_net_yds': punt_net_yds,
                            'punt_net_avg': punt_net_avg,
                            'punt_tb': punt_tb,
                            'punt_blkd': punt_blkd,
                            'punt_fc': punt_fc,
                            'punt_50+': punt_50_plus,
                            'punt_inside_20': punt_in_20,
                            'punt_long': punt_long

                        },
                            index=[0]
                        )

                        punts_df = pd.concat(
                            [punts_df, row_df], ignore_index=True)

                        del row_df
                        del punt_no, \
                            punt_gross_yds, punt_gross_avg, \
                            punt_net_yds, punt_net_avg, \
                            punt_tb, punt_blkd, \
                            punt_fc, punt_50_plus, \
                            punt_in_20, punt_long

                    elif key == "pr":  # Punt Return Stats

                        pr_no = int(value['_attributes']['no'])
                        pr_yds = int(value['_attributes']['yds'])
                        pr_td = int(value['_attributes']['td'])
                        pr_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'pr_no': pr_no,
                            'pr_yds': pr_yds,
                            'pr_td': pr_td,
                            'pr_long': pr_long

                        },
                            index=[0]
                        )

                        punt_returns_df = pd.concat(
                            [punt_returns_df, row_df], ignore_index=True)

                        del row_df
                        del pr_no, pr_yds, \
                            pr_td, pr_long

                    elif key == "kr":  # Kick Return Stats

                        kr_no = int(value['_attributes']['no'])
                        kr_yds = int(value['_attributes']['yds'])
                        kr_td = int(value['_attributes']['td'])
                        kr_long = int(value['_attributes']['long'])

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'kr_no': kr_no,
                            'kr_yds': kr_yds,
                            'kr_td': kr_td,
                            'kr_long': kr_long,
                        },
                            index=[0]
                        )

                        kick_returns_df = pd.concat(
                            [kick_returns_df, row_df], ignore_index=True)

                        del row_df
                        del kr_no, kr_yds, \
                            kr_td, kr_long

                    elif key == "fgr":  # Missed FG Return Stats

                        fgr_no = int(value['_attributes']['no'])
                        fgr_yds = int(value['_attributes']['yds'])
                        try:
                            fgr_td = int(value['_attributes']['td'])
                        except:
                            fgr_td = 0
                        try:
                            fgr_long = int(value['_attributes']['long'])
                        except:
                            fgr_long = 0

                        row_df = pd.DataFrame({
                            'season': game_season,
                            'game_id': game_id,
                            'team_id': visitor_id,
                            'team_name': visitor_name,
                            'loc': team_location,
                            'opponent_id': home_id,
                            'opponent_name': home_name,
                            'player_uni': player_uni,
                            'player_name': player_name,
                            'player_short_name': player_short_name,
                            'player_check_name': player_check_name,
                            'player_GP': player_GP,
                            'player_GS': player_GS,
                            'player_pos': player_pos,
                            'fgr_no': fgr_no,
                            'fgr_yds': fgr_yds,
                            'fgr_td': fgr_td,
                            'fgr_long': fgr_long
                        },
                            index=[0]
                        )

                        fg_returns_df = pd.concat(
                            [fg_returns_df, row_df], ignore_index=True)

                        del row_df
                        del fgr_no, fgr_yds,\
                            fgr_td, fgr_long

                    else:
                        raise ValueError(f'Unhandled Data Key:\n{key}')

    default_cols_list = [
        'season',
        'game_id',
        'team_id',
        'team_name',
        'loc',
        'opponent_id',
        'opponent_name',
        'player_uni',
        'player_name',
        'player_short_name',
        'player_check_name',
        'player_GP',
        'player_GS',
        'player_pos'
    ]

    # Passing Stats
    #############################################################################################################

    pass_df.loc[pass_df['pass_att'] > 0,
                'pass_comp_pct'] = pass_df['pass_comp'] / pass_df['pass_att']
    pass_df['pass_comp_pct'] = pass_df['pass_comp_pct'].round(2)

    pass_df.loc[pass_df['pass_att'] > 0,
                'pass_ypa'] = pass_df['pass_yds'] / pass_df['pass_att']
    pass_df['pass_ypa'] = pass_df['pass_ypa'].round(2)

    pass_df.loc[pass_df['pass_comp'] > 0,
                'pass_ypc'] = pass_df['pass_yds'] / pass_df['pass_comp']
    pass_df['pass_ypc'] = pass_df['pass_ypc'].round(2)

    pass_df.loc[pass_df['pass_att'] > 0, 'pass_cfb_qbr'] = ((8.4 * pass_df['pass_yds']) + (
        330 * pass_df['pass_tds']) + (100 * pass_df['pass_comp']) - (200*pass_df['pass_int'])) / pass_df['pass_att']
    pass_df['pass_cfb_qbr'] = pass_df['pass_cfb_qbr'].round(2)

    pass_df.loc[pass_df['pass_att'] > 0, 'pass_nfl_qbr'] = 0
    pass_df['pass_nfl_qbr'] = pass_df['pass_nfl_qbr'].round(2)

    pass_df.loc[pass_df['pass_att'] > 0, 'pass_ny/a'] = (
        pass_df['pass_yds'] - pass_df['pass_sacked_yds']) / (pass_df['pass_att'] + pass_df['pass_sacks'])
    pass_df['pass_ny/a'] = pass_df['pass_ny/a'].round(2)

    pass_df.loc[pass_df['pass_att'] > 0, 'pass_any/a'] = (
        pass_df['pass_yds'] - pass_df['pass_sacked_yds'] + (20 * pass_df['pass_tds']) - (45 * pass_df['pass_int'])) / (pass_df['pass_att'] + pass_df['pass_sacks'])
    pass_df['pass_any/a'] = pass_df['pass_any/a'].round(2)

    # Rushing Stats
    #############################################################################################################

    rush_df.loc[rush_df['rush_att'] > 0,
                'rush_avg'] = rush_df['rush_yds'] / rush_df['rush_att']
    rush_df['rush_avg'] = rush_df['rush_avg'].round(2)

    player_stats_df = pd.merge(
        left=pass_df, right=rush_df, how='outer', on=default_cols_list)

    del pass_df, rush_df

    # Rec. Stats
    #############################################################################################################

    rec_df.loc[rec_df['rec_targets'] > 0,
               'rec_catch_pct'] = rec_df['rec_no'] / rec_df['rec_targets']
    rec_df['rec_catch_pct'] = rec_df['rec_catch_pct'].round(2)
    rec_df.loc[rec_df['rec_no'] > 0,
               'rec_avg'] = rec_df['rec_yds'] / rec_df['rec_no']

    player_stats_df = player_stats_df.merge(
        right=rec_df, how='outer', on=default_cols_list)

    del rec_df

    # Fumble Stats
    #############################################################################################################

    player_stats_df = player_stats_df.merge(
        right=fumbles_df, how='outer', on=default_cols_list)

    del fumbles_df

    # Standard Defense Stats
    #############################################################################################################

    player_stats_df = player_stats_df.merge(
        right=defense_df, how='outer', on=default_cols_list)

    del defense_df

    # Interception Return Stats
    #############################################################################################################

    # ir_cols_list = default_cols_list.copy()
    # ir_cols_list.append('defense_int')
    # ir_cols_list.append('defense_int_yds')
    player_stats_df = player_stats_df.merge(
        right=interceptions_df, how='outer', on=default_cols_list)

    del interceptions_df

    # Fumble Return Stats
    #############################################################################################################
    # fr_cols_list = default_cols_list.copy()
    # fr_cols_list.append('defense_fr')
    # fr_cols_list.append('defense_fr_yds')
    player_stats_df = player_stats_df.merge(
        right=fumble_recoveries_df, how='outer', on=default_cols_list)

    del fumble_recoveries_df

    # Punting Stats
    #############################################################################################################

    player_stats_df = player_stats_df.merge(
        right=punts_df, how='outer', on=default_cols_list)

    del punts_df

    # Kickoff Stats
    #############################################################################################################

    kickoffs_df.loc[kickoffs_df['ko_no'] > 0,
                    'ko_avg'] = kickoffs_df['ko_yds'] / kickoffs_df['ko_no']
    player_stats_df = player_stats_df.merge(
        right=kickoffs_df, how='outer', on=default_cols_list)

    del kickoffs_df

    # Field Goal Stats
    #############################################################################################################

    field_goals_df.loc[field_goals_df['fg_att'] > 0,
                       'fg_pct'] = field_goals_df['fg_made']/field_goals_df['fg_att']

    player_stats_df = player_stats_df.merge(
        right=field_goals_df, how='outer', on=default_cols_list)

    del field_goals_df

    # Extra Point + 2-Point Conversion Stats
    #############################################################################################################

    player_stats_df = player_stats_df.merge(
        right=extra_points_df, how='outer', on=default_cols_list)

    del extra_points_df

    # Punt Return Stats
    #############################################################################################################

    punt_returns_df.loc[punt_returns_df['pr_no'],
                        'pr_avg'] = punt_returns_df['pr_yds'] / punt_returns_df['pr_no']

    player_stats_df = player_stats_df.merge(
        right=punt_returns_df, how='outer', on=default_cols_list)

    del punt_returns_df

    # Kick Return Stats
    #############################################################################################################
    kick_returns_df.loc[kick_returns_df['kr_no'],
                        'kr_avg'] = kick_returns_df['kr_yds'] / kick_returns_df['kr_no']

    player_stats_df = player_stats_df.merge(
        right=kick_returns_df, how='outer', on=default_cols_list)

    del kick_returns_df

    # Missed Field Goal Stats
    #############################################################################################################

    fg_returns_df.loc[fg_returns_df['fgr_no'],
                      'fgr_avg'] = fg_returns_df['fgr_yds'] / fg_returns_df['fgr_no']

    player_stats_df = player_stats_df.merge(
        right=fg_returns_df, how='outer', on=default_cols_list)

    del fg_returns_df

    player_stats_df.to_csv('test.csv')
    # # print(player_stats_df.columns)
    # print('[')
    # for c in player_stats_df.columns:
    #     print(f"\'{c}\',")
    # print(']')
    cols = [
        'season',
        'game_id',
        'team_id',
        'team_name',
        'loc',
        'opponent_id',
        'opponent_name',
        'player_uni',
        'player_name',
        'player_short_name',
        'player_check_name',
        'player_GP',
        'player_GS',
        'player_pos',
        'pass_comp',
        'pass_att',
        'pass_comp_pct',
        'pass_yds',
        'pass_tds',
        'pass_int',
        'pass_long',
        'pass_ypa',
        'pass_ypc',
        'pass_cfb_qbr',
        'pass_nfl_qbr',
        'pass_sacks',
        'pass_sacked_yds',
        'pass_ny/a',
        'pass_any/a',
        'rush_att',
        'rush_yds',
        'rush_yds_gained',
        'rush_yds_lost',
        'rush_td',
        'rush_long',
        'rush_avg',
        'rec_targets',
        'rec_no',
        'rec_yds',
        'rec_avg',
        'rec_tds',
        'rec_long',
        'rec_catch_pct',
        'fumbles',
        'fumbles_lost',
        'defense_solo_tackles',
        'defense_ast_tackles',
        'defense_total_tackles',
        'defense_solo_tfl',
        'defense_ast_tfl',
        'defense_tfls',
        'defense_tfl_yds',
        'defense_solo_sack',
        'defense_ast_sack',
        'defense_sacks',
        'defense_qb_hits',
        'defense_int',
        'defense_int_yds',
        'defense_int_td',
        'defense_int_long',
        'defense_pbu',
        'defense_ff',
        'defense_fr',
        'defense_fr_yds',
        'defense_fr_tds',
        'defense_fr_long',
        'defense_saf',
        'defense_blkd',
        'punt_no',
        'punt_gross_yds',
        'punt_gross_avg',
        'punt_net_yds',
        'punt_net_avg',
        'punt_tb',
        'punt_blkd',
        'punt_fc',
        'punt_50+',
        'punt_inside_20',
        'punt_long',
        'ko_no',
        'ko_yds',
        'ko_ob',
        'ko_tb',
        'ko_fc_yds',
        'ko_avg',
        'fg_made',
        'fg_att',
        'fg_long',
        'fg_blkd',
        'fg_pct',
        'xp_made',
        'xp_att',
        'xp_blkd',
        'two_pt_pass_made',
        'two_pt_pass_att',
        'two_pt_rush_made',
        'two_pt_rush_att',
        'two_pt_rec_made',
        'two_pt_rec_att',
        'def_two_pt_fum_made',
        'def_two_pt_fum_att',
        'def_two_pt_kick_made',
        'def_two_pt_kick_att',
        'pr_no',
        'pr_yds',
        'pr_td',
        'pr_long',
        'pr_avg',
        'kr_no',
        'kr_yds',
        'kr_td',
        'kr_long',
        'kr_avg',
        'fgr_no',
        'fgr_yds',
        'fgr_td',
        'fgr_long',
        'fgr_avg',
    ]

    player_stats_df = player_stats_df[cols]

    if save == True:
        seasons_arr = player_stats_df['season'].unique()
        for s in seasons_arr:
            season_df = player_stats_df.loc[player_stats_df['season'] == s]
            season_df.to_csv(
                f'game_stats/player/{s}_elf_player_stats.csv', index=False)

    return player_stats_df


if __name__ == "__main__":
    parse_elf_game_stats(True)

# european-league-of-football-data

Houses data related to the European League of Football (ELF).

## Repository Structure

```
european-league-of-football-data
|
├── game_stats
|   ├── player
|   └── team
|
├── gamebooks
|
├── pbp
|   ├── raw
|   ├── season
|   └── single_game
|
├── player_info
|   ├── participation_data
|   ├── photos
|   └── transactions
|
├── raw_game_data
|   ├── json
|   └── xml
|
├── rosters
|   └── raw
|
├── schedule
|
├── standings
|
└── teams

```

### Main Directory Folders:

- `game_stats`: Houses tabular season and game stats for both players and teams.
- `gamebooks`: Houses gamebooks from the ELF from previous games.
- `pbp`: Houses play-by-play (PBP) data for the ELF.
- `player_info`: Houses participation data, player headshots, and (eventually) player transaction information.
- `raw_game_data`: Holds JSON and XML files from past ELF games.
- `rosters`: Houses current and historical ELF rosters.
- `schedule`: Houses current and historical ELF schedules.
- `standings`: Houses current and historical ELF standings data.
- `teams`: Houses any and all data specifically related to ELF teams.

## Special Thanks

Special thanks to [mrcaseb](https://github.com/mrcaseb) and [his ELF data repo](https://github.com/mrcaseb/elf/tree/master) for XML data in the 2021 and 2022 seasons.

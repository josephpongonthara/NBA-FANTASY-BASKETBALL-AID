#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 17:19:38 2024

@author: josephpongonthara
"""

import json
import requests
from datetime import datetime

# Fetch JSON data
year = '2023'
url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/' + year + '/league/00_full_schedule.json'
response = requests.get(url)

# Preparing output files
fout = open("Optimized_NBAteams_gamefrequency.csv", "w")

if response.status_code == 200:
    json_data = response.json()

    # Function to extract unique team abbreviations from the JSON structure
    def extract_team_abbreviations(json_data):
        team_abbreviations = set()
        for i in range(len(json_data['lscd'])):
            for j in range(len(json_data['lscd'][i]['mscd']['g'])):
                visiting_team = json_data['lscd'][i]['mscd']['g'][j]['v']['ta']
                if isinstance(visiting_team, str) and visiting_team:
                    team_abbreviations.add(visiting_team)
                home_team = json_data['lscd'][i]['mscd']['g'][j]['h']['ta']
                if isinstance(home_team, str) and home_team:
                    team_abbreviations.add(home_team)

        return list(team_abbreviations)

    # Extract unique team abbreviations
    unique_team_abbreviations = extract_team_abbreviations(json_data)
    unique_team_abbreviations.sort()

    # Specify custom date ranges
    start_dates = [
        'Jan 1 2024', 'Jan 4 2024', 'Jan 8 2024', 'Jan 11 2024', 'Jan 15 2024',
        'Jan 18 2024', 'Jan 22 2024', 'Jan 25 2024', 'Jan 29 2024', 'Feb 1 2024',
        'Feb 5 2024', 'Feb 8 2024', 'Feb 12 2024', 'Feb 15 2024', 'Feb 19 2024',
        'Feb 22 2024', 'Feb 26 2024', 'Feb 29 2024', 'Mar 4 2024', 'Mar 7 2024',
        'Mar 11 2024', 'Mar 14 2024', 'Mar 18 2024', 'Mar 21 2024', 'Mar 25 2024',
        'Mar 28 2024', 'Apr 1 2024', 'Apr 4 2024', 'Apr 8 2024', 'Apr 11 2024'
    ]

    end_dates = [
        'Jan 3 2024', 'Jan 7 2024', 'Jan 10 2024', 'Jan 14 2024', 'Jan 17 2024',
        'Jan 21 2024', 'Jan 24 2024', 'Jan 28 2024', 'Jan 31 2024', 'Feb 4 2024',
        'Feb 7 2024', 'Feb 11 2024', 'Feb 14 2024', 'Feb 18 2024', 'Feb 21 2024',
        'Feb 25 2024', 'Feb 28 2024', 'Mar 3 2024', 'Mar 6 2024', 'Mar 10 2024',
        'Mar 13 2024', 'Mar 17 2024', 'Mar 20 2024', 'Mar 24 2024', 'Mar 27 2024',
        'Mar 31 2024', 'Apr 3 2024', 'Apr 7 2024', 'Apr 10 2024', 'Apr 14 2024'
    ]

    # Write team abbreviations to the file
    fout.write('Start Date,End Date,Most Played Teams,' + ','.join(unique_team_abbreviations) + '\n')

    # Iterate over the input date ranges
    for start_date, end_date in zip(start_dates, end_dates):
        # Convert input dates to 'YYYY-MM-DD' format
        start_date_dt = datetime.strptime(start_date, "%b %d %Y").strftime("%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%b %d %Y").strftime("%Y-%m-%d")

        # Write date range to the file
        fout.write(f'{start_date_dt},{end_date_dt},')

        # Write the number of games played for each team in the current date range
        for team in unique_team_abbreviations:
            games_played = sum(
                1 for game in json_data['lscd'] for g in game['mscd']['g'] if
                (team in [g['v']['ta'], g['h']['ta']]) and (start_date_dt <= g['gdte'] <= end_date_dt)
            )

        # Find the most played teams based on the number of games played within the range
        games_played_by_team = {team: sum(
            1 for game in json_data['lscd'] for g in game['mscd']['g'] if
            (team in [g['v']['ta'], g['h']['ta']]) and (start_date_dt <= g['gdte'] <= end_date_dt)
        ) for team in unique_team_abbreviations}
        
        max_games_played = max(games_played_by_team.values())
        most_played_teams = [team for team, games_played in games_played_by_team.items() if games_played == max_games_played]
        
        # Write the most played teams or "N/A" if the number of teams is 4 or more
        if len(most_played_teams) < 4:
            fout.write(' '.join(most_played_teams))
        else:
            fout.write('N/A')
        
        # Write the number of games played for each team in the current date range
        for team in unique_team_abbreviations:
            games_played = sum(
                1 for game in json_data['lscd'] for g in game['mscd']['g'] if
                (team in [g['v']['ta'], g['h']['ta']]) and (start_date_dt <= g['gdte'] <= end_date_dt)
            )
            fout.write(f',{games_played}')
        
        fout.write('\n')


fout.close()
response.close()

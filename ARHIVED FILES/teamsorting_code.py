#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 12:26:26 2024

@author: josephpongonthara
"""

import json
import requests

# Fetch JSON data
year = '2023'
url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/' + year + '/league/00_full_schedule.json'
response = requests.get(url)

#preparing output files
fout = open("NBAteams_sorted.csv", "w")
fout.writelines('**TEAMS**\n')


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
    #Write to the file
    fout.write('\n'.join(unique_team_abbreviations))
           
fout.close()
response.close()


# =============================================================================
#     # Print the result
#     print("Unique Team Abbreviations:", unique_team_abbreviations)
# else:
#     print("Failed to retrieve JSON data. Status code:", response.status_code)
# =============================================================================

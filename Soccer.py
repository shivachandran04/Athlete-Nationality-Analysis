import requests
import json
import time
import os
import sqlite3

def get_team_ids(football_clubs):
    ids_list = []
    for team in football_clubs:
        url = f'http://api.isportsapi.com/sport/football/team/search?api_key=EcW5k9amDCfFxIJh&name={team}'
        response = requests.get(url)
        json_string = response.content.decode('utf-8')
        dictionary = json.loads(json_string)
        if team == "Angers":
            ids_list.append(dictionary['data'][3]['teamId'])
        else:
            ids_list.append(dictionary['data'][0]['teamId'])
        time.sleep(10)
    return ids_list


def setup_teams_table(cur, conn, football_clubs):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Teams (id INTEGER PRIMARY KEY, name TEXT)"
    )
    teams = []
    for team in football_clubs:
        url = f'http://api.isportsapi.com/sport/football/team/search?api_key=EcW5k9amDCfFxIJh&name={team}'
        response = requests.get(url)
        json_string = response.content.decode('utf-8')
        dictionary = json.loads(json_string)
        print(dictionary)
        team_name = ''
        if team == "Angers":
            team_name = dictionary['data'][3]['name']
            teams.append(team_name)
        else:
            team_name = dictionary['data'][0]['name']
            teams.append(team_name)
        time.sleep(10)

    count = 0
    for team in teams:
        cur.execute("INSERT OR IGNORE INTO Teams (name) VALUES (?)", (team,))
        conn.commit()  
        if cur.rowcount != 0:
            count += 1
        if count == 25:
            break



def setup_players_table(cur, conn, ids_list):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Soccer (id INTEGER PRIMARY KEY, name TEXT, country_id INTEGER, team_id INTEGER)"
    )
    count = 0
    index = 0
    players = {}
    for ids in ids_list:
        url = f'http://api.isportsapi.com/sport/football/player?api_key=EcW5k9amDCfFxIJh&teamId={ids}'
        response = requests.get(url)
        json_string = response.content.decode('utf-8')
        dictionary = json.loads(json_string)
        print(dictionary)
        for data in dictionary['data']:
            players[data['name']] = data['country']
        time.sleep(10)
    
    for player in players:
        cur.execute("SELECT id FROM Countries WHERE Country = ?", (players[player],))
        country_id = cur.fetchone()
        team_name = football_clubs[index]
        team_name = team_name.replace('_', ' ')
        cur.execute("SELECT id FROM Teams WHERE team_name = ?", (team_name,))
        team_id = cur.fetchone()
        if country_id:
            cur.execute("INSERT OR IGNORE INTO Soccer (name, country_id, team_id) VALUES (?, ?, ?)", (data['name'], country_id[0], team_id[0]))
            conn.commit()  
            if cur.rowcount != 0:
                count += 1
        else:
            cur.execute("INSERT OR IGNORE INTO Soccer (name, country_id, team_id) VALUES (?, ?, ?)", (data['name'], -1, team_id[0]))
            conn.commit()
            if cur.rowcount != 0:
                count += 1
        if count == 25:
            break
        index += 1


def main():
    football_clubs = [
    # Bundesliga
    "Bayern_Munchen", "Borussia_Dortmund", "RB_Leipzig", "Borussia_Monchengladbach", 
    "Bayer_Leverkusen", "Eintracht_Frankfurt", "VfL_Wolfsburg", "Augsburg", 
    "TSG_Hoffenheim", "Hertha_Berlin", "FC_Koln", "SC_Freiburg", "Union_Berlin", 
    "FSV_Mainz_05", "VfB_Stuttgart", "Arminia_Bielefeld", "Schalke_04",
    # La Liga
    "Real_Madrid", "Barcelona", "Atletico_Madrid", "Sevilla", "Real_Sociedad", 
    "Villarreal", "Real_Betis", "Athletic_Bilbao", "Granada", "Valencia", 
    "Cadiz", "Levante", "Osasuna", "Getafe", "Huesca", "Real_Valladolid", 
    "Elche", "Eibar",
    # Ligue 1
    "Paris_Saint_Germain", "Marseille", "Lyon", "Monaco", "Lille", 
    "Montpellier", "Nice", "Rennes", "Reims", "Saint_Etienne", "Angers", "Brest", 
    "Metz", "Nantes", "Strasbourg", "Bordeaux", "Lorient", "Dijon", "Nimes",
    # Serie A
    "Juventus", "Inter_Milan", "AC_Milan", "Napoli", "Atalanta", "Roma", "Lazio", 
    "Sassuolo", "Verona", "Fiorentina", "Udinese", "Sampdoria", "Genoa", "Bologna", 
    "Spezia", "Cagliari", "Parma", "Torino", "Benevento", "Crotone",
    # English Premier League
    "Manchester_United", "Manchester_City", "Liverpool", "Chelsea", "Leicester_City", 
    "West_Ham_United", "Tottenham_Hotspur", "Everton", "Aston_Villa", "Arsenal", 
    "Leeds_United", "Wolves", "Crystal_Palace", "Southampton", 
    "Burnley", "Brighton_Hove_Albion", "Newcastle_United", "Fulham", 
    "West_Bromwich", "Sheffield_United"
]
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + 'temp.db')
    cur = conn.cursor()
    # ids_list = get_team_ids(football_clubs)
    setup_teams_table(cur, conn, football_clubs)
    # setup_players_table(cur, conn, ids_list)
    conn.close()

main()

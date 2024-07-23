import requests
import sqlite3

def create_table():
    """
    Create table

    Args: none

    Returns: none
    """
    conn = sqlite3.connect("countries.db")
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS NBA (
                        id INTEGER PRIMARY KEY,
                        firstname TEXT,
                        lastname TEXT,
                        country_id INTEGER
                    )''')
    conn.commit()
    conn.close()

def insert_players(player_info):
    """
    Insert player info into the table

    Args: player_info (tuple), first name, last name, country

    Returns: none
    """
    conn = sqlite3.connect("countries.db")
    curr = conn.cursor()
    for player in player_info:
        # print(player)
        usa = player[0][2]
        if usa == "USA":
            usa = "United States"
        curr.execute("SELECT id FROM Countries WHERE Country = ?", (usa,))
        country_id = curr.fetchone()
        # print(country_id)
        if country_id:
            curr.execute("INSERT OR IGNORE INTO NBA (firstname, lastname, country_id) VALUES (?, ?, ?)", (player[0][0], player[0][1], country_id[0]))
    conn.commit()
    conn.close()

def get_players():
    """
    Retrieve NBA players from a specific country from the API

    Args: country (str), country of origin

    Returns: none
    """
    data_list = []
    for i in range(1,25):
        i = str(i*25)
        url = (f"http://api.balldontlie.io/v1/players?cursor={i}&per_page=25")
        print(url)
        headers = {
            "Authorization": "0fab7ce8-dd2f-403b-b6fa-4ab027f7d18e",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        # print(data)

        # gather names and country
        for player in data["data"]:
            player_info= [(player["first_name"], player["last_name"], player["country"])]
            # print(player_info)
            if player_info not in data_list:
                print(player_info)
                data_list.append(player_info)
    print(len(data_list))
    return data_list

def main():
    create_table()
    players_list = get_players()
    insert_players(players_list)

main()
from bs4 import BeautifulSoup
import regex as re 
import requests
import os
import sqlite3



def setupDatabase(filename):
    '''
    DOCSTRING
    filename: string of the database file that we want to make. 
    Returns: cur, conn for the database.
    Description: simply creating a database.
    '''
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + filename)
    cur = conn.cursor()
    return cur, conn

def populateDatabase(data, cur, conn):
    '''
    data: list of tuples with countries and their population [(country, population)]
    cur, conn: cursos for the database
    Returns: None
    Description: Creates a table for the countries, and inserts id, the country name, and 
    population into the table. Really only needs to be run once.         
    '''
        
    #creating tables if not exist
    cur.execute("CREATE TABLE IF NOT EXISTS Countries (id INTEGER PRIMARY KEY, Country TEXT UNIQUE, Population INTEGER)")
    
    #populating the data base with an id, the country name, and the population
    counter = 0
    for i in range(len(data)):
    
        query = "SELECT * FROM Countries WHERE Country = ?"
        value = data[i][0]
        cur.execute(query, (value,))
        result = cur.fetchone()
        if result is not None:
            continue
        else:                                                        
            cur.execute("INSERT OR IGNORE INTO Countries (id, Country, Population) VALUES (?, ?, ?)",
                    (i, data[i][0], data[i][1]))
            counter += 1
            print(i, data[i][0], data[i][1])
        #limiting data entries by 25
        if counter > 25:
            break
        
    conn.commit()

def getData(soup):
    '''
    soup: Beautiful Soup for the website that we are going to scrape    
    Return: list of tuples containing information on countries and their population [(country, population)]
    Description: uses Beautiful Soup to scrape the website, and retrieves country and population.    
    '''
    #type of what we are finding 
    tables = soup.find_all('tr')
    
    data = []
    for item in tables:        
        country = item.find('a') #country
        pop = item.find('td', style="font-weight: bold;") #population
            
        if country and pop:
            #using regex to substitute ',' with blank spaces
            pop = re.sub(',', '', pop.text)
            #we need it in integer form
            pop = int(pop)
            data.append((country.text, pop))
    
    return data
        
        
def main():
    #website that we are going to scrape
    url = "https://www.worldometers.info/world-population/population-by-country/"
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    
    cur, conn = setupDatabase("countries.db")
    data = getData(soup)
    populateDatabase(data, cur, conn)
        
    conn.close()        
    
main()
    
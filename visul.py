import matplotlib.pyplot as plt
import math
import os
import sqlite3
import json

def fetch_data(conn, cur): #return 3 dictionaries         
    
    # getting country name and id together for soccer
    cur.execute("""
                SELECT Soccer.country_id, Countries.Country
                FROM Soccer
                JOIN Countries ON Soccer.country_id = Countries.id;
                """)
    country_join = cur.fetchall()
    
    # counting occurences of country
    soccer_country_count = {}
    for item in country_join:
        if item[1] not in soccer_country_count:
            soccer_country_count[item[1]] = 1
        else:
            soccer_country_count[item[1]] += 1        
    
    # sorted dictionary into another dictionary
    sorted_soccer = {k: v for k, v in sorted(soccer_country_count.items(), key=lambda item: item[1], reverse=True)}    

    
    # getting country name and id together for NBA
    cur.execute("""
            SELECT NBA.country_id, Countries.Country
            FROM NBA
            JOIN Countries ON NBA.country_id = Countries.id;
            """)
    country_join = cur.fetchall()        
    
    # counting occurences of country    
    nba_country_count = {}
    for item in country_join:
        if item[1] not in nba_country_count:
            nba_country_count[item[1]] = 1
        else:
            nba_country_count[item[1]] += 1        
    sorted_nba = {k: v for k, v in sorted(nba_country_count.items(), key=lambda item: item[1], reverse=True)}
    
    #get populations from countries table
    cur.execute("""
        SELECT Country, Population FROM Countries
    """)
    countries = cur.fetchall()   
    
    #converting list of tuples into a dictionary
    population = {}
    for country, pop in countries:
        population[country] = pop
    # print(population)
    
    return sorted_nba, sorted_soccer, population

def calculations(nba_counts, soccer_counts):
    # total players
    total_nba = 0
    nba_countries = []
    for country in nba_counts:
        total_nba += nba_counts[country]
        nba_countries.append(country)            
    
    total_soccer = 0
    soccer_countries = []
    for country in soccer_counts:
        total_soccer += soccer_counts[country]
        soccer_countries.append(country)

    
    # nba percent
    nba_perc = []
    for value in nba_counts.values():
        nba_perc.append(value/total_nba)    
            
    # soccer percent
    soccer_perc = []
    for value in soccer_counts.values():
        soccer_perc.append(value/total_soccer)
    
    # json text file
        data = {
        'nba_counts': nba_counts,
        'soccer_counts': soccer_counts,
        'nba_countries': nba_countries,
        'nba_perc': nba_perc,
        'soccer_countries': soccer_countries,
        'soccer_perc': soccer_perc
    }

    # write to JSON file
    with open('calculations.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
            
    return nba_countries, nba_perc, soccer_countries, soccer_perc
    
    
def visual_1(soccer_countries, soccer_perc):
    # barchart 
    plt.figure(figsize=(50, 10))
    countries = soccer_countries[0:40]
    players = soccer_perc[0:40]
    plt.barh(countries, players, color="blue")
    plt.xlabel("Countries")
    plt.ylabel("Percentage")
    plt.title("Percentage of Soccer Players by Country")
    plt.tight_layout()
    plt.gca().invert_yaxis() 
    plt.savefig("visual1.png")
    
def visual_2(populations, nba_counts, soccer_counts):
    # histogram professionals
    counter = {}
    for name, pop in populations.items():        
        n_count = 0
        s_count = 0
        if name in nba_counts :
            n_count = nba_counts[name]
        if name in soccer_counts:
            s_count = soccer_counts[name]
        counter[name] = (n_count + s_count) / populations[name]
    
    sorted_country = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)}                        
    plt.figure(figsize=(40, 10))
    countries = [row for row in sorted_country.keys()]
    players = [col for col in sorted_country.values()]    
    plt.bar(countries[0:40], players[0:40], color="blue")
    plt.xlabel("Countries")
    plt.ylabel("Ratio of Amount of Players and Population of their Country")
    plt.title("Ratio of Players and Country Population")
    plt.tight_layout()
    plt.savefig("visual2.png")
                
def visual_3(nba_countries, nba_perc):
    # pie chart NBA
    plt.pie(nba_perc[0:10], labels=nba_countries[0:10], autopct='%1.1f%%')
    plt.title("Percentage of NBA Players by Country")
    plt.savefig("visual3.png")    
    
def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + 'countries.db')
    cur = conn.cursor()
    nba_counts, soccer_counts, populations = fetch_data(conn, cur)
    nba_countries, nba_perc, soc_countries, soccer_perc = calculations(nba_counts, soccer_counts)
    visual_1(soc_countries, soccer_perc)
    visual_2(populations, nba_counts, soccer_counts)
    visual_3(nba_countries, nba_perc)
    conn.commit()
    conn.close()

main()

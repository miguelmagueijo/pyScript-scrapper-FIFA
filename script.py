import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3

page = requests.get("https://www.fifa.com/worldcup/matches/")
soup = BeautifulSoup(page.content, 'html.parser')
print("Code:")
print(page.status_code)
print("\n\n")

#Remove comments only to test offline
# op = open("teste.html")
# page = op.read()
# op.close()
# soup = BeautifulSoup(page, 'html.parser')

group_stage = soup.find(class_= "fi-matchlist")
items = soup.find_all(class_= "fi-mu-list")
firstgame = items[0]
# print(firstgame.prettify())

#Gets all info of matches
date = [d.get_text() for d in group_stage.select(".fi-mu__info__datetime")]
group = [g.get_text() for g in group_stage.select(".fi__info__group")]
location = [l.get_text()[1:-1] for l in group_stage.select(".fi__info__location")]
score = [s.get_text() for s in group_stage.select(".fi-s__scoreText")]
teams = [t2.get_text() for t2 in group_stage.select(".fi-t__nText")]

#Replace all \n, \r and white spaces, removes Local Time and adds UTC/GTM +1
dateF = [x.replace('\r', '').replace('\n', '').replace('      ', '').replace('Local time', ' Local time') for x in date]
groupF = [x.replace('\r', '').replace('\n', '') for x in group]
locationF = [x.replace('\r', '').replace('\n', ' - ') for x in location]
scoreF = [x.replace('\r', '').replace('\n', '').replace(' ', '') for x in score]

#Stores the length of matches
all_matches = len(date)

#Replace the time in score (game not played yet) to NULL and Goals stores the goals
Goals = []
Goals2 = []
Games = 0
for i in range(all_matches):
    if len(scoreF[i]) > 3:
        scoreF[i] = "NULL"
    if scoreF[i][:1] != "N":
        Goals.append(scoreF[i][:1])
        Goals.append(scoreF[i][-1:])
        #Goals2 is to insert on db the score of team instead of game
        Goals2.append(scoreF[i][:1])
        Goals2.append(scoreF[i][-1:])
        Games += 1
    else:
        #-1 means that the game didn't happen yet.
        Goals2.append("-1")
        Goals2.append("-1")

#Converts every string in Goals and Goals2 to INT
Goals = list(map(int, Goals))
Goals2 = list(map(int, Goals2))

#Put all values in one list.
GameInfo = [] * all_matches #Inicialize the list with 48 positions
GameN = 1
j2 = 0
for j in range(all_matches):
    GameInfo.append((groupF[j],teams[j2],scoreF[j],teams[j2+1],dateF[j],locationF[j], GameN, Goals2[j2], Goals2[j2+1]))
    j2 += 2
    GameN += 1
print(GameInfo)

#Writes in a file the information of every match
i2 = 0
f = open("FifaMatchesGroup_Stage.txt", "w")
f.write("!!!Notice that local time is the time of city where the game will be played and not your time.!!!\n\n")
for i in range(all_matches):
    f.write(groupF[i] + ": " + teams[i2] + " " + scoreF[i] + " "
     + teams[i2+1] + " - " + dateF[i] + " - " + locationF[i])
    i2 += 2
    f.write("\n\n")

#Insert gameinfo to a local db
try:
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    #Check if table FifaWorldCup does not exist and create it
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                      FifaWorldCup(id INTEGER PRIMARY KEY, MatchGroup TEXT, 
                      TeamHome TEXT, Score TEXT, TeamAway TEXT, Date TEXT, Location TEXT, GameN TEXT unique, GH INT, GA INT)''')
    #Commit the change
    db.commit()
except Exception as e:
    #Roll back any change if something goes wrong
    print("Something went wrong")
    db.rollback()
    raise e
finally:
    db.close()

#Stores GameInfo in DB
db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()
dbID = 0
try:
    with db:
        db.execute("DELETE FROM FifaWorldCup")
        db.executemany('''INSERT INTO FifaWorldCup(MatchGroup, TeamHome, Score, TeamAway, Date, Location, GameN, GH, GA)
                  VALUES(?,?,?,?,?,?,?,?,?)''', GameInfo)
        db.commit()
except Exception as e:
    #Roll back any change if something goes wrong
    print("Something went wrong")
    db.rollback()
    raise e
finally:
    db.close()

#Code to update score
# db = sqlite3.connect('db.sqlite3')
# cursor = db.cursor()
# while dbID != all_matches:
#         cursor.execute('''UPDATE FifaWorldCup SET Score = ? WHERE id = ?''', (scoreF[dbID], dbID+1))
#         dbID += 1
# db.commit()
# print("Scores updated")

print("\n\n\n\n\n")
#Gets values from db and print it
db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()
cursor.execute('''SELECT MatchGroup, TeamHome, Score, TeamAway, Date, Location FROM FifaWorldCup''')
all_rows = cursor.fetchall()
for row in all_rows:
    #Gets the row from every row in db. 0 to the first column, 1 to the second etc
    print('{0}: {1} {2} {3}, {4} in {5}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
db.close()
import pandas as pd
import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.fifa.com/worldcup/matches/")
soup = BeautifulSoup(page.content, 'html.parser')
print(page.status_code)

group_stage = soup.find(class_= "fi-matchlist")
items = soup.find_all(class_= "fi-mu-list")
firstgame = items[0]
#print(firstgame.prettify())

date = firstgame.find(class_= "fi-mu__info__datetime").get_text()
group = firstgame.find(class_= "fi__info__group").get_text()
location = firstgame.find(class_ = "fi__info__location").get_text()
score = firstgame.find(class_= "fi-s__scoreText").get_text()
teams = firstgame.find(class_= "fi-t__nText").get_text()

date = [d.get_text() for d in group_stage.select(".fi-mu__info__datetime")]
group = [g.get_text() for g in group_stage.select(".fi__info__group")]
location = [l.get_text()[1:-1] for l in group_stage.select(".fi__info__location")]
score = [s.get_text() for s in group_stage.select(".fi-s__scoreText")]
teams = [t2.get_text() for t2 in group_stage.select(".fi-t__nText")]

#Replace all \n, \r and white spaces, removes Local Time and adds UTC/GTM +1
dateF = [x.replace('\r', '').replace('\n', '').replace('      ', '').replace('Local time', ' UTC/GMT +1') for x in date]
groupF = [x.replace('\r', '').replace('\n', '') for x in group]
locationF = [x.replace('\r', '').replace('\n', ' - ') for x in location]
scoreF = [x.replace('\r', '').replace('\n', '').replace(' ', '') for x in score]

#Replace the time in score (game not played yet) to NULL
p = 0
while p != 48:
    if len(scoreF[p]) > 3:
        scoreF[p] = "NULL"
    p += 1

#Put all values in one list.
GameInfo = [[]] * 48 #Inicialize the list with 48 positions
j = 0
j2 = 0
while j != 48:
    GameInfo[j] = [(groupF[j],dateF[j],teams[j2],scoreF[j],teams[j2+1],locationF[j])]
    j += 1
    j2 += 2 
print(GameInfo)

#Writes in a file the information of every match
i = 0
i2 = 0
f = open("FifaMatchesGroup_Stage.txt", "w")
while i != 48:
    f.write(dateF[i])
    f.write("\n")
    f.write(groupF[i])
    f.write("\n")
    f.write(locationF[i])
    f.write("\n")
    f.write(teams[i2])
    i2 += 1
    f.write(" " + scoreF[i])
    f.write(" " + teams[i2])
    i += 1
    i2 += 1
    f.write("\n\n\n")
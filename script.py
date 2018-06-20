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
#team1 = firstgame.find(class_= "fi-t fi-i--4 home").get_text()
score = firstgame.find(class_= "fi-s__scoreText").get_text()
teams = firstgame.find(class_= "fi-t__n").get_text()

"""print(date)
print(group)
print(location)
print(team1)
print(team2)"""

date = [d.get_text() for d in group_stage.select(".fi-mu__info__datetime")]
group = [g.get_text() for g in group_stage.select(".fi__info__group")]
location = [l.get_text() for l in group_stage.select(".fi__info__location")]
#team1 = [g.get_text() for g in group_stage.select(".fi-t fi-i--4 home .fi-t__n")]
score = [s.get_text() for s in group_stage.select(".fi-s__scoreText")]
teams = [t2.get_text() for t2 in group_stage.select(".fi-t__n")]

print(location[1])

i = 0
i2 = 0
f = open("FifaMatchesGroup_Stage.txt", "w")
while i != 48:
    f.write(date[i])
    f.write(group[i])
    f.write(location[i])
    f.write(teams[i2])
    i2 += 1
    f.write(score[i])
    f.write(teams[i2])
    i += 1
    i2 += 1
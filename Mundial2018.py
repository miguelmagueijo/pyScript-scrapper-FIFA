import sqlite3
from script import Goals, teams, Games
import time

#Separates the output of script.py
print("\nOutput from script.py.")
print("\n" * 10)
print("Output now is from Query.py.\n\n")

def SortByGroup():
    Test = True
    while Test:
        search = input("Grupo (A/B/C/D/E/F/G/H): ").upper()
        if search in ("A", "B", "C", "D", "E", "F", "G", "H"):
            search = "Group " + search
            Test = False
        else:
            print("Enter a valid letter!\n")
    #Print games by user group input
    for row in cursor.execute("SELECT * FROM FifaWorldCup WHERE MatchGroup = ?", (search,)):
        print('{0}: {1} {2} {3} on {4} in {5}'.format(row[1], row[2], row[3], row[4], row[5], row[6]))

def SortByAllGroups():
    #Print all  rows sorted by group
    for row in cursor.execute('SELECT * FROM FifaWorldCup ORDER BY MatchGroup'):
        print('{0} {1} {2}, {3} in {4}'.format(row[1], row[2], row[3], row[4], row[5]))

def SortByGamesTeam(Teams):
    Test = True
    print("\n\n")
    #Print games by user group input
    while Test:
        print("List of teams: ")
        print(Teams)
        search = input("Name of team (ex: Portugal, be sure the name has Capitalize letters "
                        + "and must be in english): ")
        if search in Teams:
            print("\n\n")
            for row in cursor.execute("SELECT * FROM FifaWorldCup WHERE TeamHome = ?", (search,)):
                print('{0}: {1} {2} {3} on {4} in {5}'.format(row[1], row[2], row[3], row[4], row[5], row[6]))
            for row in cursor.execute("SELECT * FROM FifaWorldCup WHERE TeamAway = ?", (search,)):
                print('{0}: {1} {2} {3} on {4} in {5}'.format(row[1], row[2], row[3], row[4], row[5], row[6]))
            Test = False
        else:
            print("\n" * 5 + "Enter a valid team name!")

def SortByLocation(Locals):
    Test = True
    while Test:
        print("All locations: ")
        print(Locals)
        search = input("\nLocation name (Please Copy & Paste from the list above without " 
                        + "\'\' to search the name of location): ")
        if search in Locals:
            #Code that is executed when is valid input
            print("\n\n")
            for row in cursor.execute("SELECT * FROM FifaWorldCup WHERE Location = ?", (search,)):
                print('{0}: {1} {2} {3} on {4} - {5}'.format(row[6], row[2], row[3], row[4], row[5], row[1]))
            Test = False
        else:
            print("\n" * 5 + "Enter a valid location!")

def SortByAllLocation():
    for row in cursor.execute("SELECT * FROM FifaWorldCup ORDER BY Location"):
        print('{0}: {1} {2} {3} on {4} - {5}'.format(row[6], row[2], row[3], row[4], row[5], row[1]))

def GoalsByTeam(Teams, Goals):
    Test = True
    golos = 0
    print("\n\n")
    #Print games by user group input
    while Test:
        print("List of teams: ")
        print(Teams)
        search = input("Name of team (ex: Portugal, be sure the name has Capitalize letters "
                        + "and must be in english): ")
        if search in Teams:
            #Code that is executed when is valid input
            j = [i for i, x in enumerate(teams) if x == search]
            try:    
                for i in range(len(j)):
                    golos += Goals[j[i]]
            except IndexError:
                print(search + ": {0}".format(golos) + " goals")
            Test = False
        else:
            print("\n" * 5 + "Enter a valid team name!")

def AvGoalsPerGame(Golos, Games):
    av = Golos / Games
    print("Average goals per game:", av)

def AvGoalsPerDay(Golos):
    av = Golos / 14
    print("Average goals per day:", av)
    
def GoalsPerGroup(Goals):
    golosG = 0
    Test = True
    for row in cursor.execute("SELECT MatchGroup, GH, GA FROM FifaWorldCup ORDER BY MatchGroup"):
        if (row[1] and row [2]) > (-1):
            golosG += row[1] + row[2]
            Test = True
        elif Test:
            print('{0}: {1}'.format(row[0], golosG))
            golosG = 0
            Test = False

def EveryGoalRegistered(Golos):
    print("Total number of goals so far:", Golos)


#Connects to db
db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()

Golos = 0
for i in range(len(Goals)):
    Golos += Goals[i]
Teams = []
for row in cursor.execute('''SELECT DISTINCT TeamHome FROM FifaWorldCup ORDER BY TeamHome'''):
    Teams.append(row[0])
Locals = []
for row in cursor.execute('''SELECT DISTINCT Location FROM FifaWorldCup ORDER BY Location'''):
    Locals.append(row[0])

Loop = True
while Loop:
    time.sleep(2)
    print("\n")
    print("1 - User Group Info | 2 - All groups by order | 3 - User Team Info | 4 - User Location Info "
            + "| 5 - All locations by order | 6 - User team goals | 7 - Average goals per game "
            + "| 8 - Average goals per day | 9 - User Group Goals | 10 - Every goal so far | 0 - Exit")
    op = input("Opção: ")
    if op == "0":
        exit()
    elif op == "1":
        print("\n" * 5)
        SortByGroup()
    elif op == "2":
        print("\n" * 5)
        SortByAllGroups()
    elif op == "3":
        print("\n" * 5)
        SortByGamesTeam(Teams)
    elif op == "4":
        print("\n" * 5)
        SortByLocation(Locals)
    elif op == "5":
        print("\n" * 5)
        SortByAllLocation()
    elif op == "6":
        print("\n" * 5)
        GoalsByTeam(Teams, Goals)
    elif op == "7":
        print("\n" * 5)
        AvGoalsPerGame(Golos, Games)
    elif op == "8":
        print("\n" * 5)
        AvGoalsPerDay(Golos)
    elif op == "9":
        print("\n" * 5)
        GoalsPerGroup(Goals)
    elif op == "10":
        print("\n" * 5)
        EveryGoalRegistered(Golos)

db.close()
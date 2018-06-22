import sqlite3
from script import Goals

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
            print("\n" * 5 + "Enter a valid team/name!")

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
    print("\n\n")
    #Print games by user group input
    while Test:
        print("List of teams: ")
        print(Teams)
        search = input("Name of team (ex: Portugal, be sure the name has Capitalize letters "
                        + "and must be in english): ")
        if search in Teams:
            #Code that is executed when is valid input
            Test = False
        else:
            print("\n" * 5 + "Enter a valid team/name!")

def GoalPerGame(Goals):
    print("ASD")

def GoalPerDay(Goals):
    print("ASD")

def GoalPerGroup(Goals):
    print("ASD")

def EveryGoalRegistered(Goals):
    print("ASD")


#Connects to db
db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()

Teams = []
for row in cursor.execute('''SELECT DISTINCT TeamHome FROM FifaWorldCup ORDER BY TeamHome'''):
    Teams.append(row[0])
Locals = []
for row in cursor.execute('''SELECT DISTINCT Location FROM FifaWorldCup ORDER BY Location'''):
    Locals.append(row[0])

#print("OPTIONS")
#op = input("Op: ")

#SortByGroup()
#SortByAllGroups()
#SortByGamesTeam(Teams)
SortByLocation(Locals)
#SortByAllLocation()
#GoalsByTeam(Teams, Goals)

db.close()
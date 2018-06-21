import sqlite3

try:
    db = sqlite3.connect('testdb.sqlite3')
    # Get a cursor object
    cursor = db.cursor()
    # Check if table users does not exist and create it
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                      FifaWorldCup(id INTEGER PRIMARY KEY, MatchGroup TEXT, Date TEXT unique,
                       TeamHome TEXT, Score TEXT, TeamAway TEXT, Location TEXT)''')
    # Commit the change
    db.commit()
# Catch the exception
except Exception as e:
    # Roll back any change if something goes wrong
    print("Something went wrong")
    db.rollback()
    raise e
finally:
    # Close the db connection
    db.close()

GameInfo  = [("Group A", "18 June", "Nigéria", "5-0", "Germany", "Ruski"),
             ("Group B", "23 June", "Naosei", "7-1", "wqeqws", "Ruski2"),
             ("Group C", "14 June", "EzClap", "3-4", "ASD", "Ruski3"),
             ("Group D", "16 June", "Wut", "0-1", "Teste", "Ruski4"),
             ("Group E", "19 June", "YaBro", "0-0", "Portugal", "Ruski5")]

print(GameInfo[1])

db = sqlite3.connect('testdb.sqlite3')
cursor = db.cursor()
try:
    with db:
        db.executemany('''INSERT INTO FifaWorldCup(MatchGroup, Date, TeamHome, Score, TeamAway, Location)
                  VALUES(?,?,?,?,?,?)''', GameInfo)
        db.commit()
except sqlite3.IntegrityError:
    print('Record already exists')
finally:
    db.close()
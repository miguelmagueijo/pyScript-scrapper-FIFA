from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

db_connect = create_engine('sqlite:///db.sqlite3')
app = Flask(__name__)
api = Api(app)

class Games(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT * from FifaWorldCup")
        return {'Games': [i for i in query.cursor.fetchall()]}

class Teams(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT DISTINCT TeamHome from FifaWorldCup ORDER BY TeamHome")
        return {'Group': [i for i in query.cursor.fetchall()]}

class Stadiums(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT DISTINCT Location from FifaWorldCup ORDER BY Location")
        return {'Stadiums': [i for i in query.cursor.fetchall()]}

class Groups(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT DISTINCT MatchGroup from FifaWorldCup ORDER BY MatchGroup")
        return {'Groups': [i for i in query.cursor.fetchall()]}

class GroupInfo(Resource):
    def get(self,g):
        db = db_connect.connect()
        g = '%' + g + '%'
        query = db.execute("SELECT * from FifaWorldCup WHERE MatchGroup LIKE (?)", (g,))
        return {"Group Info": [i for i in query.cursor.fetchall()]}

class TeamInfo(Resource):
    def get(self,t):
        db = db_connect.connect()
        t = '%' + t + '%'
        query = db.execute("SELECT * from FifaWorldCup WHERE TeamHome LIKE (?) OR TeamAway LIKE (?)", (t,t,))
        return {"Team Info": [i for i in query.cursor.fetchall()]}

class StadiumInfo(Resource):
    def get(self, s):
        db = db_connect.connect()
        s = '%' + s + '%'
        query = db.execute("SELECT * from FifaWorldCup WHERE Location LIKE  (?)", (s,))
        return {'Games in ' + s: [i for i in query.cursor.fetchall()]}

api.add_resource(Games, '/WorldGroups2018')
api.add_resource(Teams, '/Teams')
api.add_resource(Stadiums, '/Stadiums')
api.add_resource(Groups, '/Groups')
api.add_resource(GroupInfo, '/Groups/<g>')
api.add_resource(TeamInfo, '/Teams/<t>')
api.add_resource(StadiumInfo, '/Stadiums/<s>')

if __name__ == '__main__':
    app.run(port='5002')
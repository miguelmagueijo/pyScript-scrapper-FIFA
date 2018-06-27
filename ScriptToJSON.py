from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

#To run this I runned it in virutal env with all dependencies and I acess by 127.0.0.1:5002/Mundial2018

db_connect = create_engine('sqlite:///db.sqlite3')
app = Flask(__name__)
api = Api(app)

class Games(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT * from FifaWorldCup")
        return {'Games': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Teams(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT DISTINCT TeamHome from FifaWorldCup ORDER BY TeamHome")
        return {'Group': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Stadiums(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT DISTINCT Location from FifaWorldCup ORDER BY Location")
        return {'Stadiums': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Groups(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT DISTINCT MatchGroup from FifaWorldCup ORDER BY MatchGroup")
        return {'Groups': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Dates(Resource):
    def get(self):
        db = db_connect.connect()
        query = db.execute("SELECT * from FifaWorldCup ORDER BY Date")
        return {'Date games': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class GroupInfo(Resource):
    def get(self,g):
        db = db_connect.connect()
        g = '%' + g + '%'
        query = db.execute("SELECT * from FifaWorldCup WHERE MatchGroup LIKE (?)", (g,))
        return {"Group Info": [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class TeamInfo(Resource):
    def get(self,t):
        db = db_connect.connect()
        t = '%' + t + '%'
        query = db.execute("SELECT * from FifaWorldCup WHERE TeamHome LIKE (?) OR TeamAway LIKE (?)", (t,t,))
        return {"Team Info": [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class StadiumInfo(Resource):
    def get(self, s):
        db = db_connect.connect()
        s = '%' + s + '%'
        query = db.execute("SELECT * from FifaWorldCup WHERE Location LIKE (?)", (s,))
        return {'Stadium games': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class DateInfo(Resource):
    def get(self, d):
        db = db_connect.connect()
        d = '%' + d + '%'
        query = db.execute("SELECT * from FifaWorldCup WHERE Date LIKE (?)", (d,))
        return {'Date games': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

api.add_resource(Games, '/Mundial2018')
api.add_resource(Teams, '/Mundial2018/Teams')
api.add_resource(Stadiums, '/Mundial2018/Stadiums')
api.add_resource(Groups, '/Mundial2018/Groups')
api.add_resource(Dates, '/Mundial2018/Dates')
api.add_resource(GroupInfo, '/Mundial2018/Groups/<g>')
api.add_resource(TeamInfo, '/Mundial2018/Teams/<t>')
api.add_resource(StadiumInfo, '/Mundial2018/Stadiums/<s>')
api.add_resource(DateInfo, '/Mundial2018/Dates/<d>')

if __name__ == '__main__':
    app.run(port='5002')
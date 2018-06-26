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
        query = db.execute("select * from FifaWorldCup")
        return {'Games:': [i for i in query.cursor.fetchall()]}        

api.add_resource(Games, '/WorldGroups2018')

if __name__ == '__main__':
     app.run(port='5002')
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

db_connect = create_engine('sqlite:///db.sqlite3')
app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from FifaWorldCup") # This line performs query and returns json result
        return {'Games:': [i for i in query.cursor.fetchall()]}        

api.add_resource(Employees, '/WorldGroups2018') # Route_1

if __name__ == '__main__':
     app.run(port='5002')
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.BankAPI
users = db["Users"]

def user_exist(username):
    if users.find({"Username":username}).count()==0:
        return False
    return True


def pass_verify(username, password):
    if not user_exist(username):
        return False
    
    hashed_pw = users.find({"Username": username})[0]["Password"]

    


class Register(Resource):
    def post(self):
        postet_data = request.get_json()

        username = postet_data["username"]
        password = postet_data["password"]

        if user_exist(username):
            ret_json = {
                "status": "301",
                "msg": "Invalid Username"
            }
            return jsonify(ret_json)
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Own": 0,
            "Debt": 0
        })

        ret_json = {
            "status": 200,
            "msg": "You succesfuly signed up for the API"
        }

        return jsonify(ret_json)


class Transfer(Resource):
    pass


class Transfer(Resource):
    pass


class Transfer(Resource):
    pass
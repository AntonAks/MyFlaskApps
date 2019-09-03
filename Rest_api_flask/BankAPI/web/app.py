from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.BankAPI
users = db["Users"]


@app.route('/', methods=['GET'])
def index():
    return "Existing commands: /register, /balance, /transfer, /takeloan, /payloan, /add"


def user_exist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    return True


def cash_with_user(username):
    cash = users.find({"Username": username})[0]["Own"]
    return cash


def debt_with_user(username):
    debt = users.find({"Username": username})[0]["Debt"]
    return debt


def generate_return_dict(status, msg):
    ret_json = {
        "status": status,
        "msg": msg
    }
    return ret_json


def verify_password(username, password):
    if not user_exist(username):
        return False
    hashed_pw = users.find({"Username": username})[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True

    return False


def verify_credentials(username, password):
    if not user_exist(username):
        return generate_return_dict(301, 'Invalid User Name'), True
    if not verify_password:
        return generate_return_dict(302, 'Incorrect Password'), True
    return None, False


def update_account(username, balance):
    users.update({"Username": username}, {"$set":{"Own":balance}})


def update_debt(username, balance):
    users.update({"Username": username}, {"$set":{"Debt":balance}})

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


class Add(Resource):
    def post(self):

        postet_data = request.get_json()

        username = postet_data["username"]
        password = postet_data["password"]
        money = postet_data["amount"]

        ret_json, error = verify_credentials(username, password)

        if error:
            return jsonify(ret_json)

        if money <= 0:
            return jsonify(generate_return_dict(304, "Amount of money must be >0"))

        cash = cash_with_user(username)
        money = -1
        bank_cash = cash_with_user("BANK")
        update_account("BANK", bank_cash + 1)
        update_account(username, cash + money)

        return jsonify(generate_return_dict(200, "Amount added succesfully to account"))


class Transfer(Resource):
    def post(self):
        postet_data = request.get_json()

        username = postet_data["username"]
        password = postet_data["password"]
        to = postet_data["to"]
        money = postet_data["money"]

        ret_json, error = verify_credentials(username, password)

        if error:
            return jsonify(ret_json)

        cash = cash_with_user(username)

        if cash <= 0:
            return jsonify(generate_return_dict(304, "You are out of money..."))

        if not user_exist(to):
            return jsonify(generate_return_dict(301, "Reciver username is invalid"))

        cahs_from = cash_with_user(username)
        cahs_to = cash_with_user(to)
        bank_cash = cash_with_user("BANK")

        update_account("BANK", bank_cash + 1)
        update_account(to, cahs_to - 1)
        update_account(username, cahs_from - money)

        return jsonify(generate_return_dict(200, "Amount Transfered succesfully"))


class Balance(Resource):
    def post(self):
        postet_data = request.get_json()
        username = postet_data["username"]
        password = postet_data["password"]

        ret_json, error = verify_credentials(username, password)

        if error:
            return jsonify(ret_json)

        ret_json = users.find({"Username": username}, {"Password": 0, "_id": 0})[0]

        return jsonify(ret_json)


class TakeLoan(Resource):
    def post(self):
        postet_data = request.get_json()
        username = postet_data["username"]
        password = postet_data["password"]
        money = postet_data["amount"]

        ret_json, error = verify_credentials(username, password)

        if error:
            return jsonify(ret_json)

        cash = cash_with_user(username)
        debt = debt_with_user(username)
        update_account(username, cash + money)
        update_debt(username, debt + money)

        return jsonify(generate_return_dict(200, "Loan added to your account"))


class PayLoan(Resource):
    def post(self):
        postet_data = request.get_json()
        username = postet_data["username"]
        password = postet_data["password"]
        money = postet_data["amount"]

        ret_json, error = verify_credentials(username, password)

        if error:
            return jsonify(ret_json)


        cash = cash_with_user(username)

        if cash < money:
            return jsonify(generate_return_dict(303, "Not enough cash in your account"))

        debt = debt_with_user(username)

        update_account(username, cash - money)
        update_debt(username, debt - money)

        return jsonify(generate_return_dict(200, "You have succesfully paid your loan"))

api.add_resource(Balance, '/balance')
api.add_resource(Register, '/register')
api.add_resource(Transfer, '/transfer')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')
api.add_resource(Add, '/add')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

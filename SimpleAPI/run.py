import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from tools import check_posted_data

app = Flask(__name__)
api = Api(app)

class Add(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data)

        if status_code != 200:
            result_map = {
                'Message': 'An error happened',
                'StatusCode': status_code
            }
            return jsonify(result_map)

        x = int(posted_data['x'])
        y = int(posted_data['y'])

        result = x + y 

        result_map = {
            'Message': result,
            'StatusCode': status_code
        }

        return jsonify(result_map)

class Substract(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data)

        if status_code != 200:
            result_map = {
                'Message': 'An error happened',
                'StatusCode': status_code
            }
            return jsonify(result_map)

        x = int(posted_data['x'])
        y = int(posted_data['y'])

        result = x - y 

        result_map = {
            'Message': result,
            'StatusCode': status_code
        }

        return jsonify(result_map)

class Multiply(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data)

        if status_code != 200:
            result_map = {
                'Message': 'An error happened',
                'StatusCode': status_code
            }
            return jsonify(result_map)

        x = int(posted_data['x'])
        y = int(posted_data['y'])

        result = x * y 

        result_map = {
            'Message': result,
            'StatusCode': status_code
        }

        return jsonify(result_map)

class Divide(Resource):
    def post(self):
        posted_data = request.get_json()
        status_code = check_posted_data(posted_data, "divide")

        if status_code != 200:
            result_map = {
                'Message': 'An error happened',
                'StatusCode': status_code
            }
            return jsonify(result_map)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        
        try:
            result = x / y 
        except ZeroDivisionError:
            status_code = 302
            result = 'ZeroDivisionError: division by zero'

        result_map = {
            'Message': result,
            'StatusCode': status_code
        }

        return jsonify(result_map)

api.add_resource(Add, "/add")
api.add_resource(Divide, "/division")
api.add_resource(Multiply, "/multiply")
api.add_resource(Substract, "/substract")

@app.route('/')
def home_page():
    return "Welcome to my first simple Flask API. Try to use next commands:"


if __name__ == "__main__":
    app.debug = False
    HOST = os.environ.get('IP', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host=HOST, port=PORT)

import os
from flask import Flask, render_template, request

app = Flask(__name__)
api = Api(app)


@app.route('/')
def start_app():
    return 'Hello from Flask!'


if __name__ == "__main__":
    app.debug = False
    HOST = os.environ.get('IP', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host=HOST, port=PORT)
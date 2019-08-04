"""
Simple Quiz test
This App start Flask application with simple quiz.
Questions and answers stored in JSON file
"""
import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """
    Index function for render main start page
    """
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    """
    Function for render quiz test page
    """
    if request.method == 'POST':
        print(request.form['answerOption'])

    return render_template('quiz_page.html')


if __name__ == '__main__':

    app.debug = True
    HOST = os.environ.get('IP', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host=HOST, port=PORT)

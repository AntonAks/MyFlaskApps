"""
Simple Quiz test
This App start Flask application with simple quiz.
Questions and answers stored in JSON file
"""
import os
from flask import Flask, render_template, request
from tools import Question

questions = Question.get_questions()
gen = Question.get_question(questions)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """
    Index function for render main start page
    """
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    from werkzeug.exceptions import BadRequestKeyError
    """
    Function for render quiz test page
    """

    if request.method == 'GET':
        context = {'Question': 'Press NEXT button for start',
        'Answers':'',
        'ModeOn':0}


    if request.method == 'POST':
        try: 
            answer_option = request.form['answerOption'] 
        except BadRequestKeyError:
            answer_option = None


        question_obj = gen.__next__()
        print(answer_option)
        context = {'Question': question_obj.text_summary,
        'Answers': question_obj.answers,
        'ModeOn':1}

    return render_template('quiz_page.html', context=context)


if __name__ == '__main__':

    app.debug = True
    HOST = os.environ.get('IP', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host=HOST, port=PORT)

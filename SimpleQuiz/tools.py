"""
Tools module used for establish backend engine for quiz functionality
1. class for handling questions
2. load data from json storage
3. store results history
"""
import json
import os
import random

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'SimpleQuiz')
QUESTIONS_FILE = os.path.join(BASE_DIR, 'questions.json')

class Question:
    """
    Class Question used for handle a question instance and for load questions from json storage
    """
    def __init__(self):
        self.text_summary = ''
        self.answers = {}

    def __repr__(self):
        return f'Question instance with: text - {self.text_summary}, answers: {self.answers}'

    @staticmethod
    def get_questions():
        """
        loads questions data from json storage
        return: shuffled list of question objects
        """
        with open(QUESTIONS_FILE, 'r') as json_file:
            questions_json_data = json.load(json_file)

        questions_list = []
        for key in questions_json_data.keys():
            temp_question = Question()
            temp_question.text_summary = questions_json_data[key]['question_text']
            temp_question.answers = questions_json_data[key]['answers']
            questions_list.append(temp_question)

        shuffled_questions_list = sorted(questions_list, key=lambda k: random.random())

        return shuffled_questions_list

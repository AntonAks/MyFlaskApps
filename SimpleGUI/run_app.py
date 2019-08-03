"""
Simple Flask App for test simple GUI.
This App start Flask application and open default browser.
"""
import os
import webbrowser
import platform
import psutil
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index function for render main application
    """
    context = {'RAM': '',
               'USERS': '',
               'CPU': '',
               'OS': ''
               }

    if request.method == 'POST':
        context['RAM'] = psutil.virtual_memory()
        context['USERS'] = psutil.users()
        context['CPU'] = psutil.cpu_stats()
        context['OS'] = f'{platform.system()} - {platform.version()}'

    return render_template('index.html', context=context)


if __name__ == '__main__':

    webbrowser.open("http://127.0.0.1:8080/", new=1, autoraise=True)

    app.debug = False
    HOST = os.environ.get('IP', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host=HOST, port=PORT)

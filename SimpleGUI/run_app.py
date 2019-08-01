import os
import psutil
import platform
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
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
    app.debug = True
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)

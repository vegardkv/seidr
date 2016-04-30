import random
import sqlite3
from flask import Flask, render_template, request, jsonify
import numpy as np


DBNAME = "crawler/games.db"

app = Flask(__name__)


@app.route('/minimal')
def minimal():
    return render_template('minimal.html')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/filter', methods=['POST'])
def filter():
    data = request.form['my_posted_data']
    return jsonify({'success': True})


@app.route('/data')
def data():
    db_connection = sqlite3.connect(DBNAME)
    db_cursor = db_connection.cursor()

    db_cursor.execute('PRAGMA table_info(games)')
    db_data = db_cursor.fetchall()
    db_names = [z[1] for z in db_data]

    db_cursor.execute('SELECT * FROM games')
    db_data = db_cursor.fetchall()

    winning_jungle = 0
    winning_top = 0
    winning_middle = 0
    losing_jungle = 0
    losing_top = 0
    losing_middle = 0
    for d in db_data:
        try:
            jngl_1 = [i for i in range(30,35) if d[i]=='JUNGLE'][0]
            jngl_2 = [i for i in range(35,40) if d[i]=='JUNGLE'][0]
            mid_1 = [i for i in range(30,35) if d[i]=='MIDDLE'][0]
            mid_2 = [i for i in range(35,40) if d[i]=='MIDDLE'][0]
            top_1 = [i for i in range(30,35) if d[i]=='TOP'][0]
            top_2 = [i for i in range(35,40) if d[i]=='TOP'][0]
        except IndexError:
            continue
        winning_jungle += float(d[(jngl_1 if d[42] else jngl_2) - 20]) / len(db_data)
        winning_top += float(d[(top_1 if d[42] else top_2) - 20]) / len(db_data)
        winning_middle += float(d[(mid_1 if d[42] else mid_2) - 20]) / len(db_data)
        losing_jungle += float(d[(jngl_2 if d[42] else jngl_1) - 20]) / len(db_data)
        losing_top += float(d[(top_2 if d[42] else top_1) - 20]) / len(db_data)
        losing_middle += float(d[(mid_2 if d[42] else mid_1) - 20]) / len(db_data)

    values = [winning_jungle, winning_middle, winning_top, losing_jungle, losing_middle, losing_top]
    labels = ['jwin', 'mwin', 'twin', 'jlose', 'mlose', 'tlose']

    temp = {'random': [(1 if i < 3 else -1)*int(values[i]/2000) for i in range(6)], 'x': [i for i in range(6)]}

    # temp = {'random': [random.randint(-10, 10) for i in range(10)], 'x': [i for i in range(10)]}
    db_connection.close()
    return jsonify({'object': [{'value': temp['random'][i], 'name': temp['x'][i]} for i in temp['x']]})


if __name__ == '__main__':

    app.run(debug=True)


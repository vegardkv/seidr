import random

from flask import Flask, render_template, request, jsonify

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
    return jsonify({'random': [random.randint(0,10)*20 for i in range(50)]})



if __name__ == '__main__':
    app.run(debug=True)

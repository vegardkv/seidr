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


if __name__ == '__main__':
    app.run(debug=True)

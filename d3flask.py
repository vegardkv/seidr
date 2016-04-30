from flask import Flask, send_from_directory, url_for, render_template

app = Flask(__name__)


@app.route('/minimal')
def minimal():
    return render_template('minimal.html')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

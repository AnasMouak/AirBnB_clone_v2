#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """return Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def home2():
    """return HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def home3(text):
    """return text"""
    pure_text = text.replace('_', ' ')
    return f'C {pure_text}'


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def home4(text):
    """return text"""
    pure_text = text.replace('_', ' ')
    return f'Python {pure_text}'


@app.route('/number/<int:n>', strict_slashes=False)
def home5(n):
    """return n"""
    return f'{n} is a number'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

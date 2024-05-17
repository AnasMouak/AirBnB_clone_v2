#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """return states list"""
    states = storage.all("State").values()
    sorted_states = sorted(states, key=lambda x: x.name)
    return render_template('7-states_list.html', states=sorted_states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def amenities_states_list():
    """return states ans amenity list"""
    states = storage.all("State").values()
    sorted_states = sorted(states, key=lambda x: x.name)
    amenities = storage.all("Amenity").values()
    sorted_amenities = sorted(amenities, key=lambda x: x.name)
    return render_template('10-hbnb_filters.html', states=sorted_states,
                           amenities=sorted_amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from app import app
import clasterize
import json
from flask import render_template


@app.route('/')
def index():
    centres = clasterize.parse_json("./app/static/AO_centres.json")
    raw_data = clasterize.parse_json("./app/static/Polyclinics.json")

    result = clasterize.clasterize(raw_data)

    return render_template('index.html', data_centres=centres, data_clasters=result)

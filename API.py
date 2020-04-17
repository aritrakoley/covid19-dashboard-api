from flask import Flask, jsonify
from data_scraper import get_formatted_data

app = Flask(__name__)

@app.route('/getData')
def get_data():
    json_data = jsonify(get_formatted_data(0))
    return json_data

from flask import Flask, jsonify
from data_scraper import get_formatted_data

app = Flask(__name__)

@app.route('/getJson')
def get_json():
    json_data = jsonify(get_formatted_data(0))
    return json_data

# if __name__ == '__main__':
#     app.run()
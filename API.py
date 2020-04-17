from flask import Flask, jsonify
from data_scraper import get_formatted_data

app = Flask(__name__)

@app.route('/')
def get_json():
    return "<h1> Heroku App Test </h1>"
    # json_data = jsonify(get_formatted_data(0))
    # return json_data

# if __name__ == '__main__':
#     app.run()
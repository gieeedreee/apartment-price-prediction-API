import pickle
import json
from flask import Flask
from flask import request

from database import database
from preprocessing import process_input

app = Flask(__name__)

with open("model/clf.pkl", "rb") as f:
    clf = pickle.load(f)


@app.route("/", methods=["GET"])
def ping() -> str:
    return "Hello Hello!"


# Creating route for model prediction
@app.route("/predict", methods=["POST"])
def predict() -> (str, int):
    """ Takes requested data from API, reaches model and send its outputs as a response into PostgreSQL
    database hosted by Heroku.
    :return: list of predicted prices
    """
    input_params, input_df = process_input(request.data)
    try:
        prediction = clf.predict(input_params)
        database.insert_into_table(input_df, prediction)
        return json.dumps({"predicted_price": prediction.tolist()})

    except ValueError:
        return json.dumps({"error": "PREDICTION FAILED"}), 400


@app.route("/select", methods=["GET"])
def get_records() -> str:
    """ Selects and returns 10 most recent requests and responses in JSON format.
    :return: data of 10 most recent requests and responses
    """
    records = database.select_from_table()
    return json.dumps({"Last 10 records": records})


if __name__ == "__main__":
    app.run(debug=True)

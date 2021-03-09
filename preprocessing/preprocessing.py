import pickle
import json
import numpy as np
import pandas as pd



class Preprocessor:
    def __init__(self):
        with open("model/encoder.pkl", "rb") as f:
            self.encoder = pickle.load(f)
        with open("model/scaler.pkl", "rb") as s:
            self.scaler = pickle.load(s)


def process_input(request_data: str) -> np.array:
    """
    Requested data is encoded, scaled and prepared for further  use.
    :return: input values and encoded/ scaled values
    """
    try:
        input_df = pd.DataFrame(json.loads(request_data)["features"])
        scaled_input = scaler.transform(input_df[['Area', 'Room', 'Year', 'Flat_floor', 'Total_floor']])
        encoded_input = pd.DataFrame(encoder.transform(input_df[['City']]))
        final_input = np.concatenate([scaled_input, encoded_input], axis=-1, )

        return final_input, input_df
    except ValueError:
        raise


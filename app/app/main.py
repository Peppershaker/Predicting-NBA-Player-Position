import os
import pickle
import pandas as pd
from flask import request, jsonify, Flask

app_root = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, root_path=app_root)

def load_pickled_model():
    """Loads and returns the pickled model to be used for prediction"""
    with open("model/trained_rf_0.774_aug_16.pickle", 'rb') as f:
        model = pickle.load(f)

    return model


@app.route('/predict', methods=['POST'])
def process_post_api_call():
    """Makes prediction and returns response in JSON. Supports
    multi row data input.

    Payload must be in JSON format.
    """

    request_data = request.data

    X = pd.read_json(request_data, orient='records').values

    prediction = model.predict(X)
    prediction_df = pd.DataFrame(prediction, columns=['y_pred'])
    prediction_json = prediction_df.to_json(orient='records')

    return prediction_json, 200

model = load_pickled_model()

import pickle
import pandas as pd

# Import the pre-trained ML model from the pickle file once at the startup, not on every request
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

MODEL_VERSION = "1.0.0"

def predict_output(user_input:dict):
    input_df = pd.DataFrame([user_input])
    prediction = model.predict(input_df)[0]
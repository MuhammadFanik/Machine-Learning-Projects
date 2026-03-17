from fastapi import FastAPI
from schema.user_input import UserInput
from model.predict import MODEL_VERSION
from fastapi.responses import JSONResponse
import pandas as pd
from starlette.responses import JSONResponse
from model.predict import  predict_output

app = FastAPI()

# Home endpoint
@app.get("/")
def home():
    return {"message": "Insurance premium prediction application"}

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "OK", "model": MODEL_VERSION}

# The Predict endpoint. When a post request hits /predict: FastAPI validates all the incoming JSON using UserInput, computed fields are calculated automatically, A Dataframe is built with only features that the model expects.
# model.predict() runs and returns the insurance_prem_category and the result is sent back as JSON
@app.post("/predict")
def predict(data: UserInput):
    user_input = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "city_tier": data.city_tier,
        "lifestyle_risk": data.lifestyle_risk,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={"predicted_category": prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
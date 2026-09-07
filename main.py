import uvicorn
from fastapi import HTTPException,FastAPI
from fastapi.responses import JSONResponse
import pickle
import joblib
from schema.user_input import UserInput
import pandas as pd
from schema.predictions import preprocess_user_input
from miscellaneous.preprosessing import BankFeatureEngineering
from pydantic import BaseModel, computed_field,Field,field_validator
from typing import Dict, Annotated, Literal

MODEL_PATH = "models/model.pkl"

MODEL = joblib.load(MODEL_PATH)

MODEL_VERSION = "1.0.0"
app= FastAPI()



@app.get("/")
def home():
     return {"message":"Home page for Banking churn prediction website"}
    

@app.get("/health")
def health_check():
     return {
          "status":"OK",
          "Model_version":MODEL_VERSION,
          "model_loaded":MODEL is not None}
     

@app.post("/predict")
def predictions(data:UserInput):
    df= preprocess_user_input(data)
    
   # prediction = MODEL.predict(features_df)[0]
    churn_prediction = df.churn_prediction  
    if churn_prediction not in [0, 1]:
         raise(HTTPException(status_code=500, detail="Invalid prediction value"))
    else:
         return JSONResponse(status_code=200,
                             content={"churn_prediction": int(churn_prediction),
                             "churn_probability": float(df.churn_probability)*100})
import pandas as pd
import joblib
from schema.user_input import UserInput
from schema.response import PredictedResponse
from miscellaneous.preprosessing import BankFeatureEngineering


MODEL = joblib.load("models/model.pkl")
PREPROCESSOR = joblib.load("models/preprocessor.pkl")

def preprocess_user_input(user_input: UserInput) -> PredictedResponse:
    # Convert Pydantic object to dict
    data = user_input.model_dump()

    data['HasCrCard'] = int(data['HasCrCard'])
    data['IsActiveMember'] = int(data['IsActiveMember'])


    df = pd.DataFrame([data])
    X_new_processed = PREPROCESSOR.transform(df)

    churn_predictions = MODEL.predict(X_new_processed)
    churn_probability = MODEL.predict_proba(X_new_processed) 
    return PredictedResponse(churn_prediction=int(churn_predictions[0]),
                             churn_probability=float(churn_probability[0][1]))  



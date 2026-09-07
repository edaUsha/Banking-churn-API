from pydantic import BaseModel

class PredictedResponse(BaseModel):
    churn_prediction: int
    churn_probability:float
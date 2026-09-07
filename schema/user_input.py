from pydantic import BaseModel, computed_field,Field,field_validator
from typing import Dict, Annotated, Literal
import pandas as pd
import joblib


class UserInput(BaseModel):

    CreditScore: Annotated[int,Field(...,gt=300,lt=900,description="The credit card score of the customer")]
    Geography: Annotated[str,Field(...,description="The country user belongs to")]
    Gender: Annotated[str, Literal["Male","Female","Others"]]
    Age:Annotated[int, Field(...,gt=0,lt=120, description="age of the customer", examples=[43])]
    Tenure: Annotated[float, Field(...,description="number of years the customer has been with the bank.")]
    Balance:Annotated[float,Field(...,description="The account balance of the customer.")]
    NumOfProducts: Annotated[int,Field(...,lt=5,description="The number of bank products the customer has.")]
    IsActiveMember: Annotated[bool,Field(...,description="Indicates whether the customer is an active member")]
    HasCrCard: Annotated[bool,Field(...,description="whether the customer has a credit card")]
    EstimatedSalary: Annotated[float,Field(...,description="estimated salary of the customer")]


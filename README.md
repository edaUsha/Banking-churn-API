# Banking-Churn-Prediction

deployment link:https://banking-churn-api.onrender.com/

- created different end points for all: home page, eda page, model page, prediction page
- churn_utils has both model loaded and features loaded

idea:
can create a pydantic model for churn utlis and load the data, compute the features


pop() in predictions.py is used to rename from api names to ml model names
API names                  ML model names

credit_score       ───►    CreditScore
age                ───►    Age
tenure             ───►    Tenure
balance            ───►    Balance
products           ───►    NumOfProducts
estimated_salary   ───►    EstimatedSalary
geography          ───►    Geography
gender             ───►    Gender

summary of what I have done:

Created a preprocessing pipeline to make it easier for preprocessing the variables after getting them from pydantic model- user_input. 

The variables are passed through the preprocessing pipeline in predictions.py:
1. pydantic object was converted into a dictionary using model_dump()
2. converted the incoming bool values into int
3. created a dataframe from data
4. used the preprocessing pipeline
5. generated churn prediction and churn probability

created response.py pydantic model to give an output to this particular datatype

main.py is the fastapi application where i used different endpoints and request types. for prediction, i have used POST to retrieve the response. I used GET to retrieve data.

the variable df is passed through preprocess_user_input from predictions.py, and the data is retrieved from User_inputs

POST: Raised an HTTPException if the response is not in the given range.
returning churn prediction and churn probability from preprocessed data

A simple frontend with streamlit where the values are given as input and the response is the probability of churn and the likelyhood of churn.

we are dockerising it for local use. 
problem: both frontend.py and main.py are running in different terminals. they need to run simultaneously for them to work. which is why we are using start.sh (shellscript) to help run them simultaneously and dockerize it.

${PORT:-8501} means: use Render's PORT if it's set, otherwise fall back to 8501 for local runs. This one-line change is what makes the same image work both locally and on Render without maintaining two versions.

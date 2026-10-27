# Banking-Churn-Prediction

deployment link:https://banking-churn-api.onrender.com/


## 1. Background and Overview

Customer churn — the decision by a customer to close their account and leave — is one of the most costly challenges facing retail banks today. Acquiring a new customer costs five to seven times more than retaining an existing one.

This project addresses a direct business question: **Which customers are most likely to leave, and what can the bank do about it before they do?**

Using a dataset of 10,000 bank customers, this analysis builds a predictive model that identifies high-risk customers before they churn, enabling the bank to intervene proactively with targeted retention strategies.



## 2. Data Structure Overview

The analysis is based on a complete dataset of **10,000 customer records** with no missing values, representing a reliable and analysis-ready foundation.

| Attribute | Detail |
|---|---|
| Total Customers | 10,000 |
| Churned Customers | 2,037 (20.37%) |
| Missing Values | None |
| Total Features | 14 columns |

**Key customer attributes included:**

| Category | Features |
|---|---|
| Demographics | Age, Gender, Geography |
| Financial Profile | Credit Score, Account Balance, Estimated Salary |
| Relationship Depth | Number of Products, Tenure, Has Credit Card |
| Engagement | Is Active Member |
| Target Variable | Exited (Churned: Yes / No) |

The dataset reflects a **realistic churn imbalance** — roughly 1 in 5 customers churned — consistent with industry norms in retail banking.



## 3. Executive Summary

This project developed a machine learning model to predict which bank customers are at risk of churning.

Older customers were more likely to leave the bank, and customers in Germany had the highest churn rate among all regions. Customers who used fewer bank products or were less active also showed a greater tendency to churn. These patterns suggest the bank should pay special attention to customer groups that may need more support, better service, or more suitable offers.

## Technical Overview:

| Component          | Technology                  | Role                                                    |
| ------------------ | --------------------------- | ------------------------------------------------------- |
| Backend API        | FastAPI                     | Handles validation, routing, and predictions            |
| Request validation | Pydantic                    | Enforces expected input fields and types                |
| ML model           | XGBoost                     | Predicts churn risk                                     |
| Preprocessing      | scikit-learn-style pipeline | Prepares raw API inputs for inference                   |
| Frontend           | Streamlit                   | Provides an interactive form and displays results       |
| Containerization   | Docker                      | Packages backend and frontend for consistent deployment |
| Startup script     | start.sh                    | Runs both services together                             |
| Deployment         | Render                      | Hosts the deployed application                          |


The repository includes separate directories for data, models, and schema, with main.py for the FastAPI app and frontend.py for the Streamlit interface.

### API Design
The application exposes separate endpoints for the home page, EDA page, model page, and prediction page. It uses GET requests to retrieve information and a POST request for churn predictions.


### Deployment
The Docker image runs both the FastAPI backend and Streamlit frontend. Because the two processes normally require separate terminals, start.sh starts them together in one container.

The startup configuration uses ${PORT:-8501}, meaning it uses Render’s assigned PORT environment variable when available and falls back to port 8501 locally. This allows the same Docker image to work in both local and cloud environments.

### sepatate notes:

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

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
import pandas as pd

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model    import LogisticRegression
from sklearn.preprocessing   import StandardScaler
from sklearn.metrics         import (roc_auc_score, recall_score,accuracy_score,
                                     precision_score, classification_report,
                                     ConfusionMatrixDisplay)
from sklearn.ensemble import RandomForestClassifier

df=pd.read_csv("data/Churn_Modelling.csv")

class BankFeatureEngineering(BaseEstimator,TransformerMixin):
    def fit(self,X,y=None):
        return self

    def transform(self,X):
        df= X.copy()

        def categorize_tenure(tenure):
            if pd.isna(tenure):
                return 'Unknown'
            elif tenure <= 2:
                return 'New (<2 yrs)'
            elif tenure <= 5:
                return 'Short-term (2-5 yrs)'
            elif tenure <= 8:
                return 'Medium-term (6-8 yrs)'
            else:
                return 'Long-term (>8 yrs)'
        
        def categorize_balance(balance):
            if pd.isna(balance):
                return 'Unknown'
            elif balance == 0:
                return 'Zero Balance'
            elif balance < 50000:
                return 'Low (<50K)'
            elif balance < 150000:
                return 'Medium (50K-150K)'
            else:
                return 'High (>150K)'
        
        
        def categorize_credit_score(CreditScore):
            if pd.isna(CreditScore):
                return 'Unknown'
            elif CreditScore<400:
                return 'Low Credit'
            elif CreditScore<550:
                return 'Okay Credit'
            elif CreditScore<650:
                return 'Good credit'
            else:
                return 'Excellent'
        
        
        
        def age_group(age):
            if pd.isna(age):
                return 'Unknown'
            elif age<30:
                return 'Young'
            elif age<45:
                return 'Adult'
            elif age<60:
                return 'Middle-Aged'
            else:
                return 'Senior'
        
        df['TenureGroup'] = df['Tenure'].apply(categorize_tenure)
        df['CreditScore Range']= df['CreditScore'].apply(categorize_credit_score)
        df['BalanceGroup'] = df['Balance'].apply(categorize_balance)
        df['AgeGroup']= df['Age'].apply(age_group)

        cols_to_drop= ['RowNumber', 'CustomerId', 'Surname']
        df= df.drop(columns=[col for col in cols_to_drop if col in df.columns])
        return df

numerical_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
categorical_cols = ['Geography', 'Gender', 'HasCrCard', 'IsActiveMember', "TenureGroup",'AgeGroup', 'BalanceGroup', 'CreditScore Range']

# standardising and converting cat to nums
numeric_transformer= Pipeline(steps=[('scaler',StandardScaler())])
categorical_transformer= Pipeline(steps=[('onehot',OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

preprocessor= ColumnTransformer(
    transformers=[
        ('num',numeric_transformer,numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ]
)


full_preprocessing_pipeline = Pipeline(steps=[
    ('feature_engineering', BankFeatureEngineering()),
    ('preprocessor', preprocessor)
])

X = df.drop('Exited', axis=1)
y = df['Exited']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size    = 0.20,
    random_state = 42,
    stratify     = y
)

# Fit & transform on training data
X_train_processed = full_preprocessing_pipeline.fit_transform(X_train)
X_test_processed = full_preprocessing_pipeline.transform(X_test)

model=RandomForestClassifier(random_state=42)
model.fit(X_train_processed,y_train)
y_pred = model.predict(X_test_processed)

# Probabilities
rf_prob = model.predict_proba(X_test_processed)[:, 1]

# Custom threshold

threshold = 0.35

rf_pred= (rf_prob >= threshold).astype(int)

 
print(f"AUC-ROC : {roc_auc_score(y_test, rf_prob):.4f}")
print(f"Recall  : {recall_score(y_test, rf_pred):.4f}")
print(f"Precision: {precision_score(y_test, rf_pred):.4f}")
print(f"\nClassification Report:")
print(classification_report(y_test, rf_pred, target_names=["Not Churned", "Churned"]))


import joblib
joblib.dump(
    full_preprocessing_pipeline,
    "models/preprocessor.pkl"
)

joblib.dump(
    model,
    "models/model.pkl"
)

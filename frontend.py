import streamlit as st
import requests

# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Banking Churn Prediction",
    page_icon="🏦",
    layout="centered"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🏦 Banking Churn Prediction")
st.write("Enter customer details to predict whether the customer is likely to churn.")

st.divider()

# --------------------------------------------------
# Input Form
# --------------------------------------------------

with st.form("customer_form"):

    st.subheader("Customer Information")

    col1, col2 = st.columns(2)

    with col1:
        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            value=650,
            step=1
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=35,
            step=1
        )

        tenure = st.number_input(
            "Tenure (years)",
            min_value=0.0,
            value=5.0,
            step=1.0
        )

        balance = st.number_input(
            "Account Balance",
            min_value=0.0,
            value=50000.0,
            step=1000.0
        )

        estimated_salary = st.number_input(
            "Estimated Salary",
            min_value=0.0,
            value=50000.0,
            step=1000.0
        )

    with col2:
        geography = st.selectbox(
            "Geography",
            ["France", "Spain", "Germany"]
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Others"]
        )

        products = st.number_input(
            "Number of Products",
            min_value=0,
            max_value=4,
            value=1,
            step=1
        )

        active = st.checkbox(
            "Active Member",
            value=True
        )

        card = st.checkbox(
            "Has Credit Card",
            value=True
        )

    st.divider()

    submitted = st.form_submit_button(
        "🔮 Predict Churn",
        use_container_width=True
    )


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if submitted:

    payload = {
    "CreditScore": credit_score,
    "Geography": geography,
    "Gender": gender,
    "Age": age,
    "Tenure": tenure,
    "Balance": balance,
    "NumOfProducts": products,
    "IsActiveMember": active,
    "HasCrCard": card,
    "EstimatedSalary": estimated_salary
}

    try:
        with st.spinner("Making prediction..."):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=10
            )

        if response.status_code == 200:

            result = response.json()
            churn_prediction = result["churn_prediction"]
            churn_probability = result.get("churn_probability")

            st.divider()
            st.subheader("Prediction Result")

            if churn_prediction == 1:
                st.error(
                    "⚠️ Customer is likely to churn"
                )

                st.write(
                    "The model predicts that this customer may leave the bank."
                )

            else:
                st.success(
                    "✅ Customer is unlikely to churn"
                )

                st.write(
                    "The model predicts that this customer is likely to stay."
                )

            st.metric(
            label="Churn Probability",
            value=f"{churn_probability:.2f}%"
            )


        else:
            st.error(
                f"API Error: {response.status_code}"
            )

            try:
                st.json(response.json())
            except Exception:
                st.write(response.text)

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI server. "
            "Make sure your FastAPI application is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The request timed out. Please try again."
        )

    except Exception as e:

        st.error(
            f"Unexpected error: {str(e)}"
        )

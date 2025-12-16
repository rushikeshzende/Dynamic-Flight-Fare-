# ✈️ Dynamic Flight Fare Prediction System

The Dynamic Flight Fare Prediction System is a machine learning–based project that predicts airline ticket prices using historical flight data. Flight fares vary frequently due to factors such as airline, route, journey date, duration, and number of stops. This project aims to reduce uncertainty in airfare pricing by learning patterns from past data and providing reliable fare predictions in advance.

The system follows a complete end-to-end machine learning pipeline. Historical flight data is cleaned and preprocessed, important temporal features are extracted from date and time fields, and categorical variables such as airline, source, and destination are encoded. Exploratory data analysis is performed to understand pricing trends, seasonal variations, and the impact of different flight characteristics on ticket prices.

Multiple regression models are trained and evaluated, including Linear Regression, Decision Tree Regressor, and Random Forest Regressor. Among these, the Random Forest model delivers the best performance by effectively capturing non-linear relationships between input features and flight fares. Model performance is evaluated using standard metrics such as R² score, Mean Absolute Error (MAE), and Root Mean Squared Error (RMSE).

The project is implemented using Python and popular data science libraries including NumPy, Pandas, Scikit-learn, Matplotlib, and Seaborn. The trained model can be saved and reused for inference and can be deployed as a web application using Flask or Streamlit. This project demonstrates the practical application of machine learning in real-world dynamic pricing systems and highlights how data-driven approaches can support smarter and more cost-effective travel decisions.

## Tech Stack
- Python
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn

## Machine Learning Models
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

# **Author**

**Rushikesh Zende**

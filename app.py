# app.py

import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load your pre-trained AI model
model = joblib.load('pcos_diagnosis_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose')
def diagnose():
    return render_template('diagnose.html')

@app.route('/identify')
def diagnose():
    return render_template('identify.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Assuming the dataset is in the same directory and named 'PCOS_data_without_infertility.xlsx'
        PCOS_inf = pd.read_csv('PCOS_infertility.csv')
        PCOS_woinf = pd.read_excel('PCOS_data_without_infertility.xlsx', sheet_name="Full_new")

        data = pd.merge(PCOS_woinf, PCOS_inf, on='Patient File No.', suffixes={'', '_y'}, how='left')

        # Dropping the repeated features after merging
        data = data.drop(['Unnamed: 44', 'Sl. No_y', 'PCOS (Y/N)_y', '  I   beta-HCG(mIU/mL)_y',
                          'II    beta-HCG(mIU/mL)_y', 'AMH(ng/mL)_y'], axis=1)
        data["AMH(ng/mL)"] = pd.to_numeric(data["AMH(ng/mL)"], errors='coerce')
        data["II    beta-HCG(mIU/mL)"] = pd.to_numeric(data["II    beta-HCG(mIU/mL)"], errors='coerce')

        # Dealing with missing values. Filling NA values with the median of that feature.
        data['Marraige Status (Yrs)'].fillna(data['Marraige Status (Yrs)'].median(), inplace=True)
        data['II    beta-HCG(mIU/mL)'].fillna(data['II    beta-HCG(mIU/mL)'].median(), inplace=True)
        data['AMH(ng/mL)'].fillna(data['AMH(ng/mL)'].median(), inplace=True)
        data['Fast food (Y/N)'].fillna(data['Fast food (Y/N)'].median(), inplace=True)

        # Clearing up the extra space in the column names (optional)
        data.columns = [col.strip() for col in data.columns]

        X = data.drop(["PCOS (Y/N)", "Sl. No", "Patient File No."], axis=1)  # dropping out index from features too

        # Predict using your AI model
        predictions = model.predict(X)

        # Return the predictions as JSON
        return jsonify({'predictions': predictions.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5500)

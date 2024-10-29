import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

# Load the fraud data from CSV
fraud_data = pd.read_csv('path_to_your_fraud_data.csv')

@app.route('/api/summary', methods=['GET'])
def get_summary():
    total_transactions = len(fraud_data)
    total_frauds = fraud_data['is_fraud'].sum()
    fraud_percentage = (total_frauds / total_transactions) * 100 if total_transactions > 0 else 0
    
    summary = {
        'total_transactions': total_transactions,
        'total_frauds': total_frauds,
        'fraud_percentage': fraud_percentage
    }
    return jsonify(summary)

@app.route('/api/fraud_cases_over_time', methods=['GET'])
def get_fraud_cases_over_time():
    fraud_data['date'] = pd.to_datetime(fraud_data['transaction_date'])  # Assuming there's a date column
    fraud_cases_over_time = fraud_data.resample('M', on='date').sum().reset_index()
    return jsonify(fraud_cases_over_time.to_dict(orient='records'))

@app.route('/api/fraud_by_device', methods=['GET'])
def get_fraud_by_device():
    fraud_by_device = fraud_data.groupby('device_type')['is_fraud'].sum().reset_index()
    return jsonify(fraud_by_device.to_dict(orient='records'))

@app.route('/api/fraud_by_geolocation', methods=['GET'])
def get_fraud_by_geolocation():
    fraud_by_geo = fraud_data.groupby('country')['is_fraud'].sum().reset_index()
    return jsonify(fraud_by_geo.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)

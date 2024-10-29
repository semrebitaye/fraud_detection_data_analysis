import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import requests

app = dash.Dash(__name__)

# Fetch data from Flask API
def fetch_data(endpoint):
    response = requests.get(endpoint)
    return response.json()

# Layout for the Dash app
app.layout = html.Div([
    html.H1("Fraud Detection Dashboard"),
    html.Div(id='summary'),
    dcc.Graph(id='fraud_cases_over_time'),
    dcc.Graph(id='fraud_by_device'),
    dcc.Graph(id='fraud_by_geolocation')
])

# Callback to update summary statistics
@app.callback(
    dash.dependencies.Output('summary', 'children'),
    [dash.dependencies.Input('summary', 'children')]
)
def update_summary(_):
    summary = fetch_data('http://127.0.0.1:5000/api/summary')
    return html.Div([
        html.Div(f"Total Transactions: {summary['total_transactions']}"),
        html.Div(f"Total Fraud Cases: {summary['total_frauds']}"),
        html.Div(f"Fraud Percentage: {summary['fraud_percentage']:.2f}%")
    ])

# Callback for fraud cases over time
@app.callback(
    dash.dependencies.Output('fraud_cases_over_time', 'figure'),
    [dash.dependencies.Input('fraud_cases_over_time', 'id')]
)
def update_fraud_cases_over_time(_):
    fraud_cases = fetch_data('http://127.0.0.1:5000/api/fraud_cases_over_time')
    dates = [entry['date'] for entry in fraud_cases]
    fraud_counts = [entry['is_fraud'] for entry in fraud_cases]
    
    return {
        'data': [go.Scatter(x=dates, y=fraud_counts, mode='lines+markers')],
        'layout': go.Layout(title='Fraud Cases Over Time', xaxis={'title': 'Date'}, yaxis={'title': 'Number of Fraud Cases'})
    }

# Callback for fraud by device
@app.callback(
    dash.dependencies.Output('fraud_by_device', 'figure'),
    [dash.dependencies.Input('fraud_by_device', 'id')]
)
def update_fraud_by_device(_):
    fraud_by_device = fetch_data('http://127.0.0.1:5000/api/fraud_by_device')
    device_types = [entry['device_type'] for entry in fraud_by_device]
    fraud_counts = [entry['is_fraud'] for entry in fraud_by_device]

    return {
        'data': [go.Bar(x=device_types, y=fraud_counts)],
        'layout': go.Layout(title='Fraud Cases by Device', xaxis={'title': 'Device Type'}, yaxis={'title': 'Number of Fraud Cases'})
    }

# Callback for fraud by geolocation
@app.callback(
    dash.dependencies.Output('fraud_by_geolocation', 'figure'),
    [dash.dependencies.Input('fraud_by_geolocation', 'id')]
)
def update_fraud_by_geolocation(_):
    fraud_by_geo = fetch_data('http://127.0.0.1:5000/api/fraud_by_geolocation')
    countries = [entry['country'] for entry in fraud_by_geo]
    fraud_counts = [entry['is_fraud'] for entry in fraud_by_geo]

    return {
        'data': [go.Bar(x=countries, y=fraud_counts)],
        'layout': go.Layout(title='Fraud Cases by Geolocation', xaxis={'title': 'Country'}, yaxis={'title': 'Number of Fraud Cases'})
    }

if __name__ == '__main__':
    app.run_server(debug=True)

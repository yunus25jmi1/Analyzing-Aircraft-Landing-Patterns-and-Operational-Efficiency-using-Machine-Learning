import os
import json
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, dash_table


def load_data():
    data_path = os.path.join('data', 'cleaned_data.csv')
    df = pd.read_csv(data_path)
    # convert source date column to datetime and create a monthly activity period
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['Activity Period'] = df['date']
    else:
        # fallback if another column exists
        try:
            df['Activity Period'] = pd.to_datetime(df['Activity Period'])
        except Exception:
            df['Activity Period'] = pd.to_datetime(df.iloc[:, 0])
    return df


df = load_data()

monthly_landings = df.groupby('Activity Period')['landings'].sum().reset_index()

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Aircraft Landing Patterns and Operational Efficiency Dashboard'),
    dcc.Tabs([
        dcc.Tab(label='Data Overview', children=[
            html.H3('Dataset Summary'),
            html.Div(f'Total records: {len(df)}'),
            html.Div(f"Date range: {monthly_landings['Activity Period'].min().strftime('%Y-%m')} to {monthly_landings['Activity Period'].max().strftime('%Y-%m')}") ,
            html.H4('Sample Data'),
            dash_table.DataTable(
                data=df.head(10).to_dict('records'),
                columns=[{"name": c, "id": c} for c in df.head(10).columns],
                page_size=10,
                style_table={'overflowX': 'auto'}
            )
        ]),

        dcc.Tab(label='Visualizations', children=[
            html.H3('Monthly Aircraft Landings'),
            dcc.Graph(
                id='landings-time',
                figure=px.line(monthly_landings, x='Activity Period', y='landings', title='Monthly Aircraft Landings')
            ),
            html.H3('Landing Count Distribution'),
            dcc.Graph(id='dist', figure=px.histogram(df, x='landings', nbins=30, title='Distribution of Landing Counts')),
            html.H3('Top Aircraft Types'),
            dcc.Graph(id='types', figure=px.bar(df['Landing Aircraft Type'].value_counts().reset_index().rename(columns={'index':'Landing Aircraft Type', 'Landing Aircraft Type':'Count'}).head(10), x='Landing Aircraft Type', y='Count', title='Top 10 Aircraft Types'))
        ]),

        dcc.Tab(label='Predictions', children=[
            html.H3('Forecast (calls API)'),
            html.Div([
                dcc.Input(id='periods-input', type='number', value=12, min=1, step=1),
                html.Button('Get Forecast', id='forecast-btn')
            ]),
            dcc.Loading(id='loading-forecast', children=[html.Pre(id='forecast-output', style={'whiteSpace':'pre-wrap'})]),
            html.H3('Anomalies'),
            html.Button('Detect Anomalies', id='anomaly-btn'),
            dcc.Loading(children=[html.Pre(id='anomaly-output', style={'whiteSpace':'pre-wrap'})]),
            html.H3('Trend Analysis'),
            html.Button('Get Trend', id='trend-btn'),
            dcc.Loading(children=[html.Pre(id='trend-output', style={'whiteSpace':'pre-wrap'})])
        ])
    ])
])


@app.callback(Output('forecast-output', 'children'), Input('forecast-btn', 'n_clicks'), State('periods-input','value'))
def fetch_forecast(n_clicks, periods):
    if not n_clicks:
        return ''
    try:
        # API expects POST with JSON body {"months": <int>}
        resp = requests.post('http://localhost:8000/forecast', json={"months": int(periods)}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return json.dumps(data, indent=2)
        return f'API error: {resp.status_code} - {resp.text}'
    except Exception as e:
        return f'Error: {e}'


@app.callback(Output('anomaly-output', 'children'), Input('anomaly-btn', 'n_clicks'))
def fetch_anomalies(n_clicks):
    if not n_clicks:
        return ''
    try:
        # Anomaly endpoint expects a POST with JSON {"value": float}
        # We'll send the last monthly landing mean as a sample value
        sample_value = float(df['landings'].mean())
        resp = requests.post('http://localhost:8000/anomaly', json={"value": sample_value}, timeout=10)
        if resp.status_code == 200:
            return json.dumps(resp.json(), indent=2)
        return f'API error: {resp.status_code} - {resp.text}'
    except Exception as e:
        return f'Error: {e}'


@app.callback(Output('trend-output', 'children'), Input('trend-btn', 'n_clicks'))
def fetch_trend(n_clicks):
    if not n_clicks:
        return ''
    try:
        resp = requests.get('http://localhost:8000/trend', timeout=10)
        if resp.status_code == 200:
            return json.dumps(resp.json(), indent=2)
        return f'API error: {resp.status_code} - {resp.text}'
    except Exception as e:
        return f'Error: {e}'


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
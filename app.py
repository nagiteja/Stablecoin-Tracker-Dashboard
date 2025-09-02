import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import asyncio
import threading
import time
from datetime import datetime, timedelta
import json

from data_collectors import DataAggregator
from config import STABLECOINS, ANOMALY_THRESHOLD

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stablecoin Tracker Dashboard"

# Initialize data aggregator
data_aggregator = DataAggregator()

# Global data storage
current_data = {}
historical_data = {}

def update_data():
    """Update data in background thread"""
    global current_data, historical_data
    
    while True:
        try:
            # Collect current data
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            current_data = loop.run_until_complete(data_aggregator.collect_all_data())
            loop.close()
            
            # Collect historical data for each stablecoin
            for symbol in STABLECOINS.keys():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                hist_data = loop.run_until_complete(data_aggregator.get_historical_data(symbol))
                if not hist_data.empty:
                    historical_data[symbol] = hist_data
                loop.close()
                
        except Exception as e:
            print(f"Error updating data: {e}")
        
        time.sleep(300)  # Update every 5 minutes

# Start background data update thread
data_thread = threading.Thread(target=update_data, daemon=True)
data_thread.start()

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🪙 Stablecoin Tracker Dashboard", 
                    className="text-center mb-4 text-primary"),
            html.P("Real-time monitoring of USDT, USDC, and DAI peg stability and supply metrics",
                   className="text-center text-muted mb-4")
        ])
    ]),
    
    # Status Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id=f"price-{symbol}", className="card-title"),
                    html.P(f"{symbol} Price", className="card-text"),
                    html.Small(id=f"change-{symbol}", className="text-muted")
                ])
            ], className="mb-3", id=f"card-{symbol}")
        ]) for symbol in STABLECOINS.keys()
    ], className="mb-4"),
    
    # Charts Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Price Charts & Anomaly Detection", className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='stablecoin-selector',
                        options=[{'label': symbol, 'value': symbol} for symbol in STABLECOINS.keys()],
                        value='USDT',
                        className="mb-3"
                    ),
                    dcc.Graph(id='price-chart', style={'height': '500px'})
                ])
            ])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Supply Metrics", className="mb-0")
                ]),
                dbc.CardBody([
                    html.Div(id='supply-metrics')
                ])
            ]),
            
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Peg Stability Analysis", className="mb-0")
                ]),
                dbc.CardBody([
                    html.Div(id='stability-analysis')
                ])
            ], className="mt-3")
        ], width=4)
    ]),
    
    # Data Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Detailed Metrics", className="mb-0")
                ]),
                dbc.CardBody([
                    html.Div(id='metrics-table')
                ])
            ])
        ])
    ], className="mt-4"),
    
    # Refresh indicator
    dbc.Row([
        dbc.Col([
            html.Div(id='last-updated', className="text-center text-muted mt-3")
        ])
    ]),
    
    # Interval component for auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=30000,  # 30 seconds
        n_intervals=0
    )
], fluid=True, className="py-4")

# Callbacks
@app.callback(
    [Output(f"price-{symbol}", "children") for symbol in STABLECOINS.keys()] +
    [Output(f"change-{symbol}", "children") for symbol in STABLECOINS.keys()],
    [Input('interval-component', 'n_intervals')]
)
def update_price_cards(n):
    """Update price cards with current data"""
    prices = []
    changes = []
    
    for symbol in STABLECOINS.keys():
        if current_data and 'prices' in current_data and symbol.lower() in current_data['prices']:
            price_data = current_data['prices'][symbol.lower()]
            price = price_data.get('usd', 0)
            change_24h = price_data.get('usd_24h_change', 0)
            
            # Color coding based on peg deviation
            deviation = abs(price - 1.0)
            if deviation > ANOMALY_THRESHOLD:
                price_color = "text-danger"
            elif deviation > 0.005:  # 0.5% deviation
                price_color = "text-warning"
            else:
                price_color = "text-success"
            
            prices.append(html.Span(f"${price:.4f}", className=price_color))
            
            change_text = f"24h: {change_24h:+.2f}%"
            change_color = "text-success" if change_24h >= 0 else "text-danger"
            changes.append(html.Span(change_text, className=change_color))
        else:
            prices.append("Loading...")
            changes.append("")
    
    return prices + changes

@app.callback(
    Output('price-chart', 'figure'),
    [Input('stablecoin-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_price_chart(selected_stablecoin, n):
    """Update price chart with historical data and anomaly detection"""
    if selected_stablecoin not in historical_data or historical_data[selected_stablecoin].empty:
        return go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    df = historical_data[selected_stablecoin].copy()
    
    # Detect anomalies
    anomalies = data_aggregator.detect_anomalies(df['price'].tolist(), ANOMALY_THRESHOLD)
    df['anomaly'] = anomalies
    
    # Create subplot for price and volume
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f'{selected_stablecoin} Price Over Time', 'Peg Deviation'),
        row_heights=[0.7, 0.3]
    )
    
    # Price line
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            name='Price',
            line=dict(color='#1f77b4', width=2)
        ),
        row=1, col=1
    )
    
    # Target price line
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=[1.0] * len(df),
            mode='lines',
            name='Target ($1.00)',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ),
        row=1, col=1
    )
    
    # Anomaly points
    anomaly_df = df[df['anomaly']]
    if not anomaly_df.empty:
        fig.add_trace(
            go.Scatter(
                x=anomaly_df['timestamp'],
                y=anomaly_df['price'],
                mode='markers',
                name='Anomaly',
                marker=dict(color='red', size=8, symbol='x')
            ),
            row=1, col=1
        )
    
    # Peg deviation
    deviation = abs(df['price'] - 1.0)
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=deviation * 100,  # Convert to percentage
            mode='lines',
            name='Deviation (%)',
            line=dict(color='#d62728', width=2),
            fill='tonexty'
        ),
        row=2, col=1
    )
    
    # Threshold line
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=[ANOMALY_THRESHOLD * 100] * len(df),
            mode='lines',
            name=f'Threshold ({ANOMALY_THRESHOLD*100:.1f}%)',
            line=dict(color='red', width=2, dash='dot')
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title=f'{selected_stablecoin} Price Analysis',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='x unified',
        showlegend=True,
        height=500
    )
    
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Deviation (%)", row=2, col=1)
    
    return fig

@app.callback(
    Output('supply-metrics', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_supply_metrics(n):
    """Update supply metrics display"""
    if not current_data or 'on_chain' not in current_data:
        return html.P("Loading supply data...")
    
    metrics = []
    for symbol, config in STABLECOINS.items():
        if symbol in current_data['on_chain']:
            data = current_data['on_chain'][symbol]
            supply = data.get('supply', 0)
            holders = data.get('holders', 0)
            
            if supply:
                supply_formatted = f"{supply:,.0f}"
            else:
                supply_formatted = "N/A"
            
            if holders:
                holders_formatted = f"{holders:,}"
            else:
                holders_formatted = "N/A"
            
            metrics.append(html.Div([
                html.H6(f"{symbol} Supply", className="text-primary"),
                html.P(f"Total: {supply_formatted}", className="mb-1"),
                html.P(f"Holders: {holders_formatted}", className="mb-3 text-muted")
            ]))
    
    return metrics

@app.callback(
    Output('stability-analysis', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_stability_analysis(n):
    """Update stability analysis display"""
    if not current_data or 'prices' not in current_data:
        return html.P("Loading stability data...")
    
    analysis = []
    for symbol in STABLECOINS.keys():
        if symbol.lower() in current_data['prices']:
            price_data = current_data['prices'][symbol.lower()]
            price = price_data.get('usd', 0)
            deviation = abs(price - 1.0)
            deviation_pct = deviation * 100
            
            if deviation > ANOMALY_THRESHOLD:
                status = "⚠️ Unstable"
                status_class = "text-danger"
            elif deviation > 0.005:
                status = "⚠️ Watch"
                status_class = "text-warning"
            else:
                status = "✅ Stable"
                status_class = "text-success"
            
            analysis.append(html.Div([
                html.H6(f"{symbol} Status", className="text-primary"),
                html.P(f"Deviation: {deviation_pct:.3f}%", className="mb-1"),
                html.P(status, className=f"mb-3 {status_class}")
            ]))
    
    return analysis

@app.callback(
    Output('metrics-table', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_metrics_table(n):
    """Update detailed metrics table"""
    if not current_data:
        return html.P("Loading metrics...")
    
    # Create table data
    table_data = []
    for symbol in STABLECOINS.keys():
        if symbol.lower() in current_data.get('prices', {}):
            price_data = current_data['prices'][symbol.lower()]
            on_chain_data = current_data.get('on_chain', {}).get(symbol, {})
            
            row = {
                'Symbol': symbol,
                'Price': f"${price_data.get('usd', 0):.4f}",
                '24h Change': f"{price_data.get('usd_24h_change', 0):+.2f}%",
                'Market Cap': f"${price_data.get('usd_market_cap', 0):,.0f}",
                'Supply': f"{on_chain_data.get('supply', 0):,.0f}" if on_chain_data.get('supply') else "N/A",
                'Holders': f"{on_chain_data.get('holders', 0):,}" if on_chain_data.get('holders') else "N/A"
            }
            table_data.append(row)
    
    if not table_data:
        return html.P("No data available")
    
    # Create table
    df = pd.DataFrame(table_data)
    table = dbc.Table.from_dataframe(
        df, 
        striped=True, 
        bordered=True, 
        hover=True,
        className="table-sm"
    )
    
    return table

@app.callback(
    Output('last-updated', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_last_updated(n):
    """Update last updated timestamp"""
    if current_data and 'timestamp' in current_data:
        timestamp = current_data['timestamp']
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
            return f"Last updated: {formatted_time}"
        except:
            return f"Last updated: {timestamp}"
    return "Updating..."

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

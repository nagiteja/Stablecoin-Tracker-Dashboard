import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stablecoin Tracker Dashboard"

# Sample data
sample_data = {
    'USDT': {
        'price': 1.00,
        'market_cap': 100000000000,
        'change_24h': 0.01,
        'supply': 100000000000,
        'holders': 5000000,
        'peg_deviation': 0.0,
        'status': 'Stable'
    },
    'USDC': {
        'price': 1.00,
        'market_cap': 50000000000,
        'change_24h': -0.01,
        'supply': 50000000000,
        'holders': 2000000,
        'peg_deviation': 0.0,
        'status': 'Stable'
    },
    'DAI': {
        'price': 0.999,
        'market_cap': 5000000000,
        'change_24h': -0.1,
        'supply': 5000000000,
        'holders': 1000000,
        'peg_deviation': -0.1,
        'status': 'Minor Deviation'
    }
}

# Create sample historical data
def create_sample_chart_data():
    dates = pd.date_range(start='2024-08-01', end='2024-09-02', freq='D')
    data = {}
    for symbol in ['USDT', 'USDC', 'DAI']:
        base_price = 1.0 if symbol != 'DAI' else 0.999
        prices = [base_price + (i * 0.001 * (1 if i % 2 == 0 else -1)) for i in range(len(dates))]
        data[symbol] = pd.DataFrame({'date': dates, 'price': prices})
    return data

chart_data = create_sample_chart_data()

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🪙 Stablecoin Tracker Dashboard", className="text-center mb-4"),
            html.P("Real-time monitoring of stablecoin prices and peg stability", className="text-center text-muted mb-4")
        ])
    ]),
    
    # Status Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("USDT", className="card-title"),
                    html.H2(f"${sample_data['USDT']['price']:.3f}", className="text-success"),
                    html.P(f"24h: {sample_data['USDT']['change_24h']:+.2%}", className="mb-1"),
                    html.Small(f"Market Cap: ${sample_data['USDT']['market_cap']/1e9:.1f}B", className="text-muted"),
                    html.Br(),
                    html.Small(f"Supply: {sample_data['USDT']['supply']/1e9:.1f}B", className="text-muted"),
                    html.Br(),
                    html.Small(f"Holders: {sample_data['USDT']['holders']/1e6:.1f}M", className="text-muted"),
                    html.Br(),
                    dbc.Badge("Stable", color="success", className="mt-2")
                ])
            ], className="h-100")
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("USDC", className="card-title"),
                    html.H2(f"${sample_data['USDC']['price']:.3f}", className="text-success"),
                    html.P(f"24h: {sample_data['USDC']['change_24h']:+.2%}", className="mb-1"),
                    html.Small(f"Market Cap: ${sample_data['USDC']['market_cap']/1e9:.1f}B", className="text-muted"),
                    html.Br(),
                    html.Small(f"Supply: {sample_data['USDC']['supply']/1e9:.1f}B", className="text-muted"),
                    html.Br(),
                    html.Small(f"Holders: {sample_data['USDC']['holders']/1e6:.1f}M", className="text-muted"),
                    html.Br(),
                    dbc.Badge("Stable", color="success", className="mt-2")
                ])
            ], className="h-100")
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("DAI", className="card-title"),
                    html.H2(f"${sample_data['DAI']['price']:.3f}", className="text-warning"),
                    html.P(f"24h: {sample_data['DAI']['change_24h']:+.2%}", className="mb-1"),
                    html.Small(f"Market Cap: ${sample_data['DAI']['market_cap']/1e9:.1f}B", className="text-muted"),
                    html.Br(),
                    html.Small(f"Supply: {sample_data['DAI']['supply']/1e9:.1f}B", className="text-muted"),
                    html.Br(),
                    html.Small(f"Holders: {sample_data['DAI']['holders']/1e6:.1f}M", className="text-muted"),
                    html.Br(),
                    dbc.Badge("Minor Deviation", color="warning", className="mt-2")
                ])
            ], className="h-100")
        ], width=4)
    ], className="mb-4"),
    
    # Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Price History (Last 30 Days)"),
                dbc.CardBody([
                    dcc.Graph(
                        figure={
                            'data': [
                                go.Scatter(
                                    x=chart_data[symbol]['date'],
                                    y=chart_data[symbol]['price'],
                                    mode='lines',
                                    name=symbol,
                                    line=dict(width=2)
                                ) for symbol in ['USDT', 'USDC', 'DAI']
                            ],
                            'layout': go.Layout(
                                title="Stablecoin Price Trends",
                                xaxis={'title': 'Date'},
                                yaxis={'title': 'Price (USD)', 'range': [0.995, 1.005]},
                                hovermode='x unified',
                                showlegend=True
                            )
                        }
                    )
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # Summary Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Summary Statistics"),
                dbc.CardBody([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th("Stablecoin"),
                                html.Th("Price"),
                                html.Th("24h Change"),
                                html.Th("Market Cap"),
                                html.Th("Status")
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                html.Td("USDT"),
                                html.Td(f"${sample_data['USDT']['price']:.3f}"),
                                html.Td(f"{sample_data['USDT']['change_24h']:+.2%}"),
                                html.Td(f"${sample_data['USDT']['market_cap']/1e9:.1f}B"),
                                html.Td(dbc.Badge("Stable", color="success"))
                            ]),
                            html.Tr([
                                html.Td("USDC"),
                                html.Td(f"${sample_data['USDC']['price']:.3f}"),
                                html.Td(f"{sample_data['USDC']['change_24h']:+.2%}"),
                                html.Td(f"${sample_data['USDC']['market_cap']/1e9:.1f}B"),
                                html.Td(dbc.Badge("Stable", color="success"))
                            ]),
                            html.Tr([
                                html.Td("DAI"),
                                html.Td(f"${sample_data['DAI']['price']:.3f}"),
                                html.Td(f"{sample_data['DAI']['change_24h']:+.2%}"),
                                html.Td(f"${sample_data['DAI']['market_cap']/1e9:.1f}B"),
                                html.Td(dbc.Badge("Minor Deviation", color="warning"))
                            ])
                        ])
                    ], className="table table-striped")
                ])
            ])
        ], width=12)
    ]),
    
    # Auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # Update every 5 minutes
        n_intervals=0
    )
], fluid=True)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)

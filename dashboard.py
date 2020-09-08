import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import pandas as pd
import numpy as np

# DATAFRAMES FOR CHARTS

df = pd.read_csv('orders.csv')
units_by_sku = df.groupby('sku').sum().reset_index()
new_v_repeat = df.groupby('New').sum().reset_index()
over_time = df.groupby('purchase date').sum().reset_index()
state = df.groupby('ship-state').count().reset_index()
orders_by_time = df.groupby('purchase-hour').sum().reset_index()

#EXTERNAL SOURCES FOR STYLESHEETS, LOGOS, IMAGES

external_stylesheets = [dbc.themes.YETI]

hour_to_clock = {
    '00': '12 AM',
    '01': '1 AM',
    '02': '2 AM',
    '03': '3 AM',
    '04': '4 AM',
    '05': '5 AM',
    '06': '6 AM',
    '07': '7 AM',
    '08': '8 AM',
    '09': '9 AM',
    '10': '10 AM',
    '11': '11 AM',
    '12': '12 PM',
    '13': '1 PM',
    '14': '2 PM',
    '15': '3 PM',
    '16': '4 PM',
    '17': '5 PM',
    '18': '6 PM',
    '19': '7 PM',
    '20': '8 PM',
    '21': '9 PM',
    '22': '10 PM',
    '23': '11 PM'
}

# BEGIN APP

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# FIGURE DECLARATION FOR CHARTS

units_fig = px.bar(units_by_sku, x="sku", y="quantity-shipped", color="sku", barmode="group")
new_repeat_fig = px.bar(new_v_repeat, x='New', y='quantity-shipped')
rev_ot = px.line(over_time, x=over_time['purchase date'], y=over_time['item-price'])
rev_ot.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

orders_by_state = go.Figure(data=go.Choropleth(
    locations=state['ship-state'], # Two-Letter State Codes
    z=state['quantity-shipped'].astype(int), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Blues',
    colorbar_title = "Quantity Shipped",
))

orders_by_state.update_layout(
    geo_scope='usa', # limite map scope to USA
)

time = px.scatter_polar(orders_by_time,
                       r='quantity-shipped',
                       theta=hour_to_clock.values(),
                       size='quantity-shipped',
                       color='quantity-shipped',
                       color_discrete_sequence=px.colors.sequential.dense
                      )


app.layout = html.Div([
        dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    dbc.Col(dbc.NavbarBrand("Simple Product Sales Dashboard", className="ml-2")),
                    align="center",
                    no_gutters=True,
                ),
                href="#",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
        ],
        color="dark",
        dark=True,
    ),
    html.Br(),
        dbc.Row([
            dbc.Col([
                html.H3('Revenue Over Time', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='new-v-repeat',
                    figure=rev_ot
                )
            ])
        ]
    ),
        dbc.Row(
    [
            dbc.Col([
                html.H3('Total Units Sold by SKU', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='units-by-sku2',
                    figure=units_fig
                )
            ]),
            dbc.Col([
                html.H3('New vs. Repeat Customer Units Sold', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='new-v-repeat2',
                    figure=new_repeat_fig
                )
            ])
    ]),
        dbc.Row(
    [
            dbc.Col([
                html.H3('Total Units Sold by State', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='units-by-state',
                    figure=orders_by_state
                )
            ]),
            dbc.Col([
                html.H3('Quantity Shipped by Time of Day', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='quantity-shipped-time',
                    figure=time
                )
            ])
    ]),
    dbc.Row(
        style={'backgroundColor': "#333", 'height': '50px', 'textAlign': 'center'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server


gdp = requests.get(
    "https://api.stlouisfed.org/fred/series/observations?series_id=GDPC1&api_key=7094417a738f239ea845caa840d51422&file_type=json").json()
unemp = requests.get(
    "https://api.stlouisfed.org/fred/series/observations?series_id=UNEMPLOY&api_key=7094417a738f239ea845caa840d51422&file_type=json").json()
pce = requests.get(
    "https://api.stlouisfed.org/fred/series/observations?series_id=PCE&api_key=7094417a738f239ea845caa840d51422&file_type=json").json()
debt = requests.get(
    "https://api.stlouisfed.org/fred/series/observations?series_id=GFDEBTN&api_key=7094417a738f239ea845caa840d51422&file_type=json").json()
ffr = requests.get(
    "https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key=7094417a738f239ea845caa840d51422&file_type=json").json()
m2 = requests.get(
    "https://api.stlouisfed.org/fred/series/observations?series_id=M2&api_key=7094417a738f239ea845caa840d51422&file_type=json").json()


# real gdp df cleaning
rgdp_df = pd.DataFrame(gdp["observations"])
new_rgdp_df = rgdp_df.iloc[:, 2:]
new_rgdp_df["value"] = new_rgdp_df["value"].astype("float")
new_rgdp_df["value"] = round(new_rgdp_df["value"] * 1000000000, 2)
new_rgdp_df = new_rgdp_df.rename(
    columns={"date": "Date", "value": "Real GDP"})
new_rgdp_df['year'] = pd.DatetimeIndex(new_rgdp_df['Date']).year
new_rgdp_df = new_rgdp_df[new_rgdp_df["year"] >= 2010]


# unemployment df cleaning
unemp_df = pd.DataFrame(unemp["observations"])
new_unemp_df = unemp_df.iloc[:, 2:]
new_unemp_df["value"] = new_unemp_df["value"].astype("float")
new_unemp_df["value"] = round(new_unemp_df["value"] * 1000, 2)
new_unemp_df = new_unemp_df.rename(
    columns={"date": "Date", "value": "Unemployment Level"})
new_unemp_df['year'] = pd.DatetimeIndex(new_unemp_df['Date']).year
new_unemp_df['month'] = pd.DatetimeIndex(new_unemp_df['Date']).month
new_unemp_df = new_unemp_df[new_unemp_df["year"] >= 2015]


# pce df cleaning
pce_df = pd.DataFrame(pce["observations"])
new_pce_df = pce_df.iloc[:, 2:]
new_pce_df["value"] = new_pce_df["value"].astype("float")
new_pce_df["value"] = round(new_pce_df["value"] * 1000000000, 2)
new_pce_df = new_pce_df.rename(
    columns={"date": "Date", "value": "PCE"})
new_pce_df['year'] = pd.DatetimeIndex(new_pce_df['Date']).year
new_pce_df['month'] = pd.DatetimeIndex(new_pce_df['Date']).month
new_pce_df = new_pce_df[new_pce_df["year"] >= 2015]


# debt df cleaning
debt_df = pd.DataFrame(debt["observations"])
new_debt_df = debt_df.iloc[:, 2:]
new_debt_df["value"] = new_debt_df["value"].astype("float")
new_debt_df["value"] = round(new_debt_df["value"] * 1000000, 2)
new_debt_df = new_debt_df.rename(
    columns={"date": "Date", "value": "Debt"})
new_debt_df['year'] = pd.DatetimeIndex(new_debt_df['Date']).year
new_debt_df['month'] = pd.DatetimeIndex(new_debt_df['Date']).month
new_debt_df = new_debt_df[new_debt_df["year"] >= 2010]


# ffr df cleaning
ffr_df = pd.DataFrame(ffr["observations"])
new_ffr_df = ffr_df.iloc[:, 2:]
new_ffr_df = new_ffr_df.rename(
    columns={"date": "Date", "value": "ffr"})
new_ffr_df['year'] = pd.DatetimeIndex(new_ffr_df['Date']).year
new_ffr_df['month'] = pd.DatetimeIndex(new_ffr_df['Date']).month
new_ffr_df = new_ffr_df[new_ffr_df["year"] >= 2010]


# m2 df cleaning
m2_df = pd.DataFrame(m2["observations"])
new_m2_df = m2_df.iloc[:, 2:]
new_m2_df = new_m2_df.rename(
    columns={"date": "Date", "value": "M2"})
new_m2_df['year'] = pd.DatetimeIndex(new_m2_df['Date']).year
new_m2_df['month'] = pd.DatetimeIndex(new_m2_df['Date']).month
new_m2_df = new_m2_df[new_m2_df["year"] >= 2010]



def generate_table(dataframe, max_rows=700):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe) - 1, len(dataframe) - 60, -1)
        ])
    ])


fig1 = px.line(new_rgdp_df, x="Date", y="Real GDP",
              width=450, height=450, title="Real GDP")
fig2 = px.line(new_unemp_df, x="Date", y="Unemployment Level",
              width=450, height=450, title="Unemployment Level")
fig3 = px.line(new_pce_df, x="Date", y="PCE",
              width=450, height=450, title="Personal Consumption Expenditures")
fig4 = px.line(new_debt_df, x="Date", y="Debt",
              width=450, height=450, title="US Public Debt")
fig5 = px.line(new_ffr_df, x="Date", y="ffr",
              width=450, height=450, title="US Federal Funds Rate")
fig6 = px.line(new_m2_df, x="Date", y="M2",
              width=450, height=450, title="US Money Supply (M2)")



graph1 = dcc.Graph(
    id='rgdp-graph',
    figure=fig1
)
graph2 = dcc.Graph(
    id='unemp-graph',
    figure=fig2
)
graph3 = dcc.Graph(
    id='pce-graph',
    figure=fig3
)
graph4 = dcc.Graph(
    id='debt-graph',
    figure=fig4
)
graph5 = dcc.Graph(
    id='ffr-graph',
    figure=fig5
)
graph6 = dcc.Graph(
    id='m2-graph',
    figure=fig6
)

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(graph1), md=4),
                dbc.Col(html.Div(graph2), md=4),
                dbc.Col(html.Div(graph3), md=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Slider(
                    id='rgdp-slider',
                    min=new_rgdp_df["year"].min(),
                    max=new_rgdp_df["year"].max(),
                    value=new_rgdp_df["year"].max(),
                    marks={str(year): str(year)
                           for year in new_rgdp_df['year'].unique()},
                    step=None,
                )), md=4),
                dbc.Col(html.Div(dcc.Slider(
                    id='unemp-slider',
                    min=new_unemp_df["year"].min(),
                    max=new_unemp_df["year"].max(),
                    value=new_unemp_df["year"].max(),
                    marks={str(year): str(year)
                           for year in new_unemp_df['year'].unique()}
                )), md=4),
                dbc.Col(html.Div(dcc.Slider(
                    id='pce-slider',
                    min=new_pce_df["year"].min(),
                    max=new_pce_df["year"].max(),
                    value=new_pce_df["year"].max(),
                    marks={str(year): str(year)
                           for year in new_pce_df['year'].unique()}
                )), md=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(graph4), md=4),
                dbc.Col(html.Div(graph5), md=4),
                dbc.Col(html.Div(graph6), md=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Slider(
                    id="debt-slider",
                    min=new_debt_df["year"].min(),
                    max=new_debt_df["year"].max(),
                    value=new_debt_df["year"].max(),
                    marks={str(year): str(year)
                            for year in new_debt_df['year'].unique()}
                )), md=4),
                dbc.Col(html.Div(dcc.Slider(
                    id="ffr-slider",
                    min=new_ffr_df["year"].min(),
                    max=new_ffr_df["year"].max(),
                    value=new_ffr_df["year"].max(),
                    marks={str(year): str(year)
                            for year in new_ffr_df['year'].unique()}
                )), md=4),
                dbc.Col(html.Div(dcc.Slider(
                    id="m2-slider",
                    min=new_m2_df["year"].min(),
                    max=new_m2_df["year"].max(),
                    value=new_m2_df["year"].max(),
                    marks={str(year): str(year)
                            for year in new_m2_df['year'].unique()}
                )), md=4),
            ]
        ),
    ],
)


@app.callback(
    Output('rgdp-graph', 'figure'),
    [Input('rgdp-slider', 'value')])
def update_figure(selected_year):
    filtered_df = new_rgdp_df[new_rgdp_df.year <= selected_year]

    fig = px.line(filtered_df, x="Date", y="Real GDP",
              width=450, height=450, title="Real GDP")

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('unemp-graph', 'figure'),
    [Input('unemp-slider', 'value')])
def update_figure2(selected_year):
    filtered_df = new_unemp_df[new_unemp_df.year <= selected_year]

    fig = px.line(filtered_df, x="Date", y="Unemployment Level",
              width=450, height=450, title="Unemployment Level")

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('pce-graph', 'figure'),
    [Input('pce-slider', 'value')])
def update_figure3(selected_year):
    filtered_df = new_pce_df[new_pce_df.year <= selected_year]

    fig = px.line(filtered_df, x="Date", y="PCE",
              width=450, height=450, title="PCE")

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('debt-graph', 'figure'),
    [Input('debt-slider', 'value')])
def update_figure4(selected_year):
    filtered_df = new_debt_df[new_debt_df.year <= selected_year]

    fig = px.line(filtered_df, x="Date", y="Debt",
              width=450, height=450, title="Debt")

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('ffr-graph', 'figure'),
    [Input('ffr-slider', 'value')])
def update_figure5(selected_year):
    filtered_df = new_ffr_df[new_ffr_df.year <= selected_year]

    fig = px.line(filtered_df, x="Date", y="ffr",
              width=450, height=450, title="US Federal Funds Rate")

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('m2-graph', 'figure'),
    [Input('m2-slider', 'value')])
def update_figure6(selected_year):
    filtered_df = new_m2_df[new_m2_df.year <= selected_year]

    fig = px.line(filtered_df, x="Date", y="M2",
              width=450, height=450, title="US Federal Funds Rate")

    fig.update_layout(transition_duration=500)

    return fig


app.layout = html.Div([
    html.H1("US Economy Dashboard", id="title"),
    row,
])



if __name__ == "__main__":
    app.run_server(debug=True)

# ----------- requirements -----------

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# import plotly.graph_objects as go
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
import pandas as pd
import os

# ----------- importing files -----------

dir_path = os.path.dirname(os.path.realpath(__file__))
totems = pd.read_csv(os.path.join(dir_path, 'geoinfo.csv'), index_col=0)

# ----------- initializing app -----------

# external_stylesheets=[dbc.themes.SOLAR]
app = dash.Dash(__name__)

# ----------- dash components -----------

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1('A year of biking in Montpellier',
                            className='text-center')
                    ),
            ),
    dbc.Row(dbc.Col(html.H3('Bike traffic visualization',
                            className='text-center'),
                    # width={'size': 6, 'offset': 4},
                    ),
            ),
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(dcc.Markdown('''This app is currently in construction !
                '''),
                width={'size': 11, "offset": 1}
                    )
            ),
    html.Br(),
    dbc.Row(dbc.Col(dcc.Markdown('''This app proposes a visualization of the Montpellier Méditerrannée Open Data
                relative to bike traffic, available 
                [here](https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-eco-compteurs).
                '''),
                width={'size': 11, "offset": 1}
                    )
            ),
    html.Br(),
    dbc.Row(dbc.Col(dcc.Markdown('''Scroll down to see the different options. Have fun!'''),
                        width={'size': 11, "offset": 1}
                        )
                ),
    html.Br(),
    dbc.Row(dbc.Col(dcc.Markdown('''Below is an interactive map that shows the location 
                                    of the different totems in Montpellier and surroundings. 
                                    Try to click on the markers!
                                '''),
                width={'size': 11, "offset": 1}
                    )
            ),
    dbc.Row(dbc.Col(html.Iframe(id='map',
                                srcDoc=open(os.path.join(dir_path, 'totem_map.html'), 'r').read(),
                                width='100%', height='600'),
                            width={'size': 10, 'offset': 1},
                    ),
            ),
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(dcc.Markdown('''Below is an interactive graph showing the intensity 
                                    of bike traffic around the different totems.
                                    You can select one an 'navigate' on the line chart,  
                                    zoom in and out...
                                '''),
                width={'size': 11, "offset": 1}
                    )
            ),
    dbc.Row(dbc.Col(dcc.Dropdown(id="slct_totem", multi=False, value='Tanneurs',
                 options=[
                     {"label": "Tanneurs", "value": 188609530},
                     {"label": "Berracasa", "value": 121403593},
                     {"label": "Celleneuve", "value": 734202564},
                     {"label": "Laverune", "value": 97705885},
                     {"label": "ViellePoste", "value": 676645909},
                     {"label": "Delmas", "value": 105575465},
                     {"label": "Gerhardt", "value": 23231541},
                     {"label": "Lattes2", "value": 25871951},
                     {"label": "Lattes1", "value": 137058167}],
                     placeholder="Select a totem"),
                 width={'size': 3, "offset": 2}
                 ),
            ),
    html.Br(),
    dbc.Row(dbc.Col(dcc.Graph(id='my_graph', figure={}, style={'width': "100%"}),
                    width={'size': 10, 'offset': 1}
                    ),
            ),
    html.Br()
])


# ----------- callbacks -----------

@app.callback(
    Output(component_id='my_graph', component_property='figure'),
    [Input(component_id='slct_totem', component_property='value')]
    )

def plot_laneId(selected_laneId):
    """
    Time series lineplot
    Input:
        selected_laneId: lane id associated with the totem chosen in the dropdown
    Output:
        fig: plot of daily and weekly resampled time series together
    """
    df = totems.copy()
    df = df.loc[df['laneId'] == selected_laneId]
    df['daily'] = df['intensity']
    del df['intensity']
    dfw = df.copy()
    dfw.index = pd.to_datetime(dfw.index)
    dfw['weekly'] = dfw['daily'].resample('W').mean()
    df['weekly'] = dfw['weekly']
    df.index = pd.to_datetime(df.index)
    df['weekly'] = dfw['weekly'].interpolate()
    fig = px.line(df, y=['daily', 'weekly'],
            title='Bike traffic intensity through time',
            color_discrete_sequence = ["#ca0020", "#252525"],
            template="plotly_white")
    fig = fig.update_xaxes(title_text='Date')
    fig = fig.update_yaxes(title_text='Intensity')
    fig = fig.update_layout(title_font_size=21,
                            title_x=0.50,
                            title_y=0.85,
                            legend_title_text='time basis',
                            legend_y=0.94,
                            legend_x=0.87,
                            margin_l=90)
    return fig

# ----------- running app -----------

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
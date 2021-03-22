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
    dcc.Dropdown(id="slct_totem", multi=False, value='Tanneurs',
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
                 style={'width': "40%"}
                 ),
    html.Br(),
    dcc.Graph(id='my_graph', figure={}, style={'width': "90%"}),
    html.Br(),
    dbc.Row(dbc.Col(html.Iframe(id='map',
                                srcDoc=open(os.path.join(dir_path, 'totem_map.html'), 'r').read(),
                                width='100%', height='600'),
                            width={'size': 10, 'offset': 1},
                    ),
            )
])


# ----------- callbacks -----------

@app.callback(
    Output(component_id='my_graph', component_property='figure'),
    [Input(component_id='slct_totem', component_property='value')]
    )

def plot_laneId(selected_laneId):
    dff = totems.copy()
    dff = dff.loc[dff['laneId'] == selected_laneId]
    fig = px.line(dff, y='intensity', title='Bike traffic intensity through time')
    return fig


# ----------- running app -----------

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
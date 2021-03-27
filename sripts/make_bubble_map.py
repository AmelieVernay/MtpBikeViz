# ----------- requirements -----------

import pandas as pd
import ast

import plotly.express as px


# ----------- load data -----------

geoinfo = pd.read_csv('./geoinfo.csv')
del geoinfo['id']
del geoinfo['type']
del geoinfo['vehicleType']
del geoinfo['reversedLane']


# ---------- grab coordinates ----------


# getting latitudes and longitudes
def latitude(df):
    """ grabs latitude coordinates """
    latitudes = []
    for i in range(len(df)):
        coord = ast.literal_eval(df.iloc[i, 3])
        latitudes.append(coord['coordinates'][1])
    return latitudes


def longitude(df):
    """ grabs longitude coordinates """
    longitudes = []
    for i in range(len(df)):
        coord = ast.literal_eval(df.iloc[i, 3])
        longitudes.append(coord['coordinates'][0])
    return longitudes


geoinfo['latitudes'] = latitude(geoinfo)
geoinfo['longitudes'] = longitude(geoinfo)
del geoinfo['location']


# ---------- keep only common dates ----------

df = geoinfo.copy()
df['dateObserved'] = pd.to_datetime(df['dateObserved'], format='%Y-%m-%d')
df.set_index('dateObserved', inplace=True)
least_common_date = (df.index.month >= 9)
dff = geoinfo[least_common_date]


# ---------- mabpox identification (optional) ----------

access_token = 'pk.eyJ1IjoiYW1lbGlldmVybmF5IiwiYSI6ImNrbXF1NzF1bzAxamEycHMxYjh2YWE2cDIifQ.AQcLxU02IYosV3c65nb1ZQ'
px.set_mapbox_access_token(access_token)


# ---------- plot ----------

fig = px.scatter_mapbox(
    dff, lat="latitudes", lon="longitudes",
    size="intensity", size_max=50,
    color="intensity", color_continuous_scale=px.colors.sequential.Pinkyl,
    opacity=0.5,
    hover_name="name",
    mapbox_style='dark', zoom=11.7,
    animation_frame="dateObserved", animation_group="name",
    width=1000, height=600
)

# add legend, title...
fig = fig.update_layout(
        title_text='Bike traffic intensity in Montpellier and surroundings',
        title_font_size=19,
        title_x=0.73,
        title_y=0.96,
        legend_title_text='Intensity')

# animation details
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
fig.layout.updatemenus[0].buttons[0].label = "Play"
fig.layout.updatemenus[0].buttons[1].label = "Pause"
fig.layout.coloraxis.showscale = True
fig.layout.sliders[0].pad.t = 10
fig.layout.updatemenus[0].pad.t = 10
fig.layout.coloraxis.cmin = 100
fig.layout.coloraxis.cmax = 1900

sliders = [dict(currentvalue={"prefix": "Date: "}, pad={"t": 50})]
fig = fig.update_layout(sliders=sliders)

# saving animation
fig.write_html("./bubble_map.html")

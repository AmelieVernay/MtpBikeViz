# ----------- requirements -----------

import folium
from folium import IFrame
import folium.plugins
import pandas as pd
import base64
import os

# ----------- importing files -----------

dir_path = os.path.dirname(os.path.realpath(__file__))
Coord = pd.read_csv(os.path.join(dir_path, 'coordinates.csv'), index_col=0)

# ----------- initializing map -----------

map = folium.Map(location=[43.60969924926758, 3.896939992904663],
                 zoom_start=13)

mrkClust = folium.plugins.MarkerCluster().add_to(map)

# tooltip = "Click to see image!"

for i, row in Coord.iterrows():
   Name = Coord.at[i, 'Name']
   lat = Coord.at[i, 'latitude']
   lng = Coord.at[i, 'longitude']
   folium.Marker(
       location=[lat, lng],
       popup=folium.Popup(
          '<h1><b><p style="text-align:center;">{}</p></b></h1><br>'.format(Name) +
          Coord.at[i, 'adress'] +
          '<br>' +
          '<h5><b>Record: </b></h5>{}'.format(str(Coord.at[i, 'record'])) +
          '<br>' +
          '<h5><b>Record day: </b></h5>{}'.format(Coord.at[i, 'record day']) +
          '<br>' +
          '<h5><b>Daily mean: </b></h5>{}'.format(str(Coord.at[i, 'daily mean'])),
          width=1500),
       tooltip=Name,
       icon=folium.Icon(color='red', icon='bicycle', prefix='fa')).add_to(mrkClust)

#iframe = folium.IFrame(popuptext, width=700, height=1000)
#popup = folium.Popup(iframe)
map.save(os.path.join(dir_path, 'totem_map.html'))

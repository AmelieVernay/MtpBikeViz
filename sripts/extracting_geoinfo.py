# ----------- requirements -----------

from datetime import datetime
from glob import glob
import pandas as pd
import json
import os

import matplotlib.pyplot as plt
import seaborn as sns

# ----------- importing files -----------

dir_path = os.path.dirname(os.path.realpath(__file__))

files_path = os.path.join(dir_path, 'archives')
files = glob(os.path.join(files_path, '*Archive2020.json'))

data_file = pd.read_json(files[0], lines=True)

for file in files:
    temp = pd.read_json(file, lines=True)
    data_file = pd.concat([data_file, temp], ignore_index=True)

data_file = data_file[366:]  # removing initialization doublon

# ----------- formating the date column -----------


def date_format(df):
    """
    removes hours minutes and seconds in the 'dateObserved' column,
    sets the 'dateObserved' column to datetime object,
    and makes it the index colums
    """
    for i in range(len(df)):
        df.iloc[i, 2] = df.iloc[i, 2][0:10]
    df['dateObserved'] = pd.to_datetime(df['dateObserved'])
    df.set_index('dateObserved', inplace=True)


date_format(data_file)

# ----------- adding names -----------

data_file['name'] = ''

for i in range(len(data_file)):
    if data_file['laneId'][i] == 121403593:
        data_file['name'][i] = 'Berracasa'
    if data_file['laneId'][i] == 734202564:
        data_file['name'][i] = 'Celleneuve'
    if data_file['laneId'][i] == 97705885:
        data_file['name'][i] = 'Lavérune'
    if data_file['laneId'][i] == 676645909:
        data_file['name'][i] = 'Vielle Poste'
    if data_file['laneId'][i] == 105575465:
        data_file['name'][i] = 'Delmas'
    if data_file['laneId'][i] == 23231541:
        data_file['name'][i] = 'Gerhardt'
    if data_file['laneId'][i] == 137058167:
        data_file['name'][i] = 'Lattes 1'
    if data_file['laneId'][i] == 25871951:
        data_file['name'][i] = 'Lattes 2'
    if data_file['laneId'][i] == 188609530:
        data_file['name'][i] = 'Tanneurs'

# ----------- saving to csv -----------

data_file.to_csv(os.path.join(dir_path, 'geoinfo.csv'))

# ----------- plotting part -----------
#  
#  sns.set(rc={'figure.figsize': (20, 7)})
#  palette = sns.color_palette("colorblind")
#  
#  
#  def ts_plot(df, number, name):
#      """
#      Time series lineplot
#      Inputs:
#          df: dataframe (with datetime objects in index column,
#                         and an 'intensity' column)
#          number: integer (for the image name)
#          name: string (for the title of the plot)
#      Output:
#          fig: plot of daily and weekly resampled time series together
#          saves the image
#      """
#      save_path = os.path.join(dir_path, 'images')
#  
#      weekly = df.resample('W').mean()
#      start = df.index[0]
#      end = df.index[-1]
#      # Plot daily and weekly resampled time series together
#      # daily:
#      sns.set_theme(style="whitegrid")
#      fig, ax = plt.subplots()
#      ax.plot(df.loc[start:end, 'intensity'],
#              marker='.', linestyle='-', label='Daily', color=palette[3])
#      # weekly:
#      ax.plot(weekly.loc[start:end, 'intensity'],
#              marker='o', markersize=5, linestyle='-',
#              label='Weekly Mean Resample', color=palette[0])
#      ax.set_ylabel('Bike traffic intensity', fontsize=17)
#      plt.title(name, fontsize=37)
#      ax.legend()
#      fig.savefig(os.path.join(save_path, 'im{}.png'.format(number)))
#  
#  
#  # plot and save images
#  unique = data_file['laneId'].unique()
#  
#  for i in range(len(unique)):
#      dff = data_file.copy()
#      dff = dff.loc[dff['laneId'] == unique[i]]
#      tot_name = dff['name'][i]
#      ts_plot(dff, (i + 1), tot_name)


# ----------- extracting geographic coordinates -----------

names = ['Berracasa', 'Lavérune', 'Celleneuve',
         'Lattes 2', 'Lattes 1', 'ViellePoste', 
         'Gerhardt', 'Delmas', 'Tanneurs']


# getting latitudes and longitudes
def latitude(df):
    """ grabs latitude coordinates """
    coord = df.iloc[0, 2]
    return(coord['coordinates'][1])


def longitude(df):
    """ grabs longitude coordinates """
    coord = df.iloc[0, 2]
    return(coord['coordinates'][0])


latitudes = []
longitudes = []

unique = data_file['laneId'].unique()
for i in range(len(names)):
    dff = data_file.copy()
    dff = dff.loc[dff['laneId'] == unique[i]]
    latitudes.append(latitude(dff))
    longitudes.append(longitude(dff))


# getting intensity records
record = []
record_day = []
daily_mean = []

unique = data_file['laneId'].unique()
for i in range(len(names)):
    dff = data_file.copy()
    dff = dff.loc[dff['laneId'] == unique[i]]
    rec = dff['intensity'].max()
    rec_day = dff['intensity'].idxmax().strftime("%B %d, %Y")
    d_mean = dff['intensity'].mean()
    record.append(rec)
    record_day.append(rec_day)
    daily_mean.append(round(d_mean, 2))


# getting adresses
adress = ['Allée Alegria Berracasa, Montpellier',
          'D5E1, Lavérune',
          '137 avenue de Lodève, Montpellier',
          'Avenue Georges Frêche, Perols',
          'Avenue Georges Frêche, Perols',
          '1211 rue de la Vieille-Poste, Montpellier',
          '1 rue Gerhardt, Montpellier',
          '73 Avenue François Delmas, Montpellier',
          'Place Albert 1er, Montpellier']

# defining coordinates dataframe
df_coordinates = pd.DataFrame({'Name': names,
                               'latitude': latitudes,
                               'longitude': longitudes,
                               'record': record,
                               'record day': record_day,
                               'daily mean': daily_mean,
                               'adress': adress})

# saving as csv
df_coordinates.to_csv(os.path.join(dir_path, 'coordinates.csv'))

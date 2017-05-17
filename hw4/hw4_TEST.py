import pandas as pd
import numpy as np
from bokeh.palettes import Spectral11
from bokeh.plotting import figure, show, output_file
import pandasql as pdsql

def get_data():
    df = pd.read_csv('./Data/riverkeeper_data_2013.csv')
    df['EnteroCountMOD'] = df['EnteroCount'].map(lambda x: x.lstrip('<>').rstrip('<>'))
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['EnteroCountMOD'] = pd.to_numeric(df['EnteroCountMOD'])
    df = df.sort_index(by=['Site', 'Date'], ascending=[True, True])
    return df

df = get_data()

pysql = lambda q: pdsql.sqldf(q, globals())

output_file('temp.html')


#grid = gridplot([[p1, p2], [None, p3]])
#for

import random

unique_site_names = df['Site'].unique()
site_names = random.sample(unique_site_names,  4)
 
def getPlotForName(name):    
    df_current = df[df['Site']==name]
    p = figure(plot_width=300, plot_height=200, title=name)
    
    rain =  df_current['FourDayRainTotal']
    rain_norm = (rain-min(rain))/(max(rain)-min(rain))
    entero = df_current['EnteroCountMOD']
    entero_norm = (entero-min(entero))/(max(entero)-min(entero))
    
    p.line(df['Date'], rain_norm, line_width=2, color="blue")
    p.line(df['Date'], entero_norm, line_width=2, color="red")
    
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Normalized Rain and Entero Counts'
    return (p)
    
plt_1 = getPlotForName(site_names[0]);
plt_2 = getPlotForName(site_names[1]);
plt_3 = getPlotForName(site_names[2]);
plt_4 = getPlotForName(site_names[3]);

q3_grid = gridplot([[plt_1, plt_2], [plt_3, plt_4]])
show(q3_grid)
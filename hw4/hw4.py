"""
This assignment must be done in python. It must be done using the ‘bokeh’, 'seaborn', or
'pandas' package. You may turn in either a . py file or an ipython notebook file.

@author: Dan Fanelli
"""

import pandas as pd
from bokeh.plotting import gridplot, figure
from bokeh.io import output_file, show
from bokeh.charts import Scatter, Bar
import pandasql as pdsql
from bokeh.models.widgets import Panel, Tabs
from math import pi

plt_wdth = 1200
plt_hgt = 1200

output_file("hw4.html")

def get_data():
    df = pd.read_csv('./Data/riverkeeper_data_2013.csv')
    df['EnteroCountMOD'] = df['EnteroCount'].map(lambda x: x.lstrip('<>').rstrip('<>'))
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['EnteroCountMOD'] = pd.to_numeric(df['EnteroCountMOD'])
    df = df.sort_index(by=['Site', 'Date'], ascending=[True, True])
    return df

df = get_data()
pysql = lambda q: pdsql.sqldf(q, globals())

"""
- Create lists & graphs of the best and worst places to swim in the dataset.
"""
def getQ1A():
    p1t = Scatter(df, x='Date', y='EnteroCountMOD', color='Site', title="Enterococcus levels in the Hudson River", legend="bottom_left", xlabel="Date", ylabel="Entero", tools=None, plot_width=plt_wdth, plot_height=plt_hgt)
    p1t.title.text_font_size = "20px"
    return p1t

def getQ1B():
    df_high = pysql("select Site, avg(EnteroCountMOD) as avg_entero from df group by Site order by avg_entero desc limit 5;")     
    p1t = Bar(df_high, label='Site', values='avg_entero', color="red", title="5 Highest Mean Enterococcus levels", tools=None, plot_width=plt_wdth, plot_height=plt_hgt)    
    p1t.title.text_font_size = "20px"
    return p1t

def getQ1C():
    df_low = pysql("select Site, avg(EnteroCountMOD) as avg_entero from df group by Site order by avg_entero limit 5;")     
    p1t = Bar(df_low, label='Site', values='avg_entero', color="green", title="5 Lowest Mean Enterococcus levels", tools=None, plot_width=plt_wdth, plot_height=plt_hgt)    
    p1t.title.text_font_size = "20px"
    return p1t

"""
- The testing of water quality can be sporadic. Which sites have been tested most regularly?
Which ones have long gaps between tests? Pick out 5-10 sites and visually compare how
regularly their water quality is tested.
"""
def q2Helper(ascDesc, limitNum, the_color):
    global time_between_df
    time_between_df = None    
    sites_dates = pysql("select Site, Date from df order by site, date")
    last_row = None
    for i, row in sites_dates.iterrows():
        last_row_same = False
        last_row_exists = (last_row is not None)
        if(last_row_exists):
            last_row_head_1 = last_row[['Site']].head(1).item()
            row_head_1 = row[['Site']].head(1).item()
            last_row_same = (last_row_head_1==row_head_1)
        if(last_row_exists & last_row_same):
            row_dt = row[['Date']].head(1).item()
            last_row_dt = last_row[['Date']].head(1).item()
            row_dt = pd.to_datetime(row_dt);
            last_row_dt = pd.to_datetime(last_row_dt);
            the_time_since_last = (row_dt - last_row_dt).days;
            dat = {'Site': row[['Site']], 'time_since_last': the_time_since_last}
            row_df = pd.DataFrame(dat)
            if(time_between_df is None):
                time_between_df = row_df
            else:    
                time_between_df = time_between_df.append(row_df)
        last_row = row;

    print time_between_df

    df_var = pysql("SELECT Site, count(*) as count, AVG((time_since_last - sub.a) * (time_since_last - sub.a)) as var from time_between_df, (SELECT AVG(time_since_last) AS a FROM time_between_df) AS sub group by Site order by var " + ascDesc + " limit " + str(limitNum));
    p1t = Bar(df_var, label='Site', values='var', color=the_color, title="Variance of Days Between Tests", tools=None, plot_width=plt_wdth, plot_height=plt_hgt)    
    p1t.title.text_font_size = "20px"
    p1t.xaxis.major_label_orientation = pi/2
    p1t.toolbar_location = None   
    p1t.logo = None
    return p1t

def getQ2A():
    return q2Helper('asc',1000,"orange");

def getQ2B():
    return q2Helper('desc',5,"red");

def getQ2C():
    return q2Helper('asc',5,"green");
"""
- Is there a relationship between the amount of rain and water quality? Show this
relationship graphically. If you can, estimate the effect of rain on quality at different sites and
create a visualization to compare them.
"""
import random

unique_site_names = df['Site'].unique()
site_names = random.sample(unique_site_names,  16)
 
def getPlotForName(name):    
    df_current = df[df['Site']==name]
    p = figure(plot_width=plt_wdth/4, plot_height=plt_hgt/4, title=name)
    
    rain =  df_current['FourDayRainTotal']
    rain_norm = (rain-min(rain))/(max(rain)-min(rain))
    entero = df_current['EnteroCountMOD']
    entero_norm = (entero-min(entero))/(max(entero)-min(entero))
    
    p.line(df['Date'], rain_norm, line_width=2, color="blue")
    p.line(df['Date'], entero_norm, line_width=2, color="red")
    
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Norm. Rain+Entero'
    return (p)
    
plt_1 = getPlotForName(site_names[0]);
plt_2 = getPlotForName(site_names[1]);
plt_3 = getPlotForName(site_names[2]);
plt_4 = getPlotForName(site_names[3]);
plt_5 = getPlotForName(site_names[4]);
plt_6 = getPlotForName(site_names[5]);
plt_7 = getPlotForName(site_names[6]);
plt_8 = getPlotForName(site_names[7]);
plt_9 = getPlotForName(site_names[8]);
plt_10 = getPlotForName(site_names[9]);
plt_11 = getPlotForName(site_names[10]);
plt_12 = getPlotForName(site_names[11]);
plt_13 = getPlotForName(site_names[12]);
plt_14 = getPlotForName(site_names[13]);
plt_15 = getPlotForName(site_names[14]);
plt_16 = getPlotForName(site_names[15]);

q3_grid = gridplot([[plt_1, plt_2, plt_3, plt_4],[plt_5, plt_6, plt_7, plt_8],[plt_9, plt_10, plt_11, plt_12],[plt_13, plt_14, plt_15, plt_16]])


"""
Put it all together:
"""

tab_1A = Panel(child=getQ1A(), title="All Levels")
tab_1B = Panel(child=getQ1B(), title="5 Highest")
tab_1C = Panel(child=getQ1C(), title="5 Lowest")

tabs_1 = Tabs(tabs=[tab_1A, tab_1B, tab_1C], sizing_mode='stretch_both')

tab_2A = Panel(child=getQ2A(), title="SPORADIC")
tab_2B = Panel(child=getQ2B(), title="TOP 5")
tab_2C = Panel(child=getQ2C(), title="BOTTOM 5")

tabs_2 = Tabs(tabs=[tab_2A, tab_2B, tab_2C])

tab_3 = Panel(child=q3_grid, title="Correlation: Rain+Entero")
tabs_3 = Tabs(tabs=[tab_3])

plt_grid = gridplot([[tabs_1],[tabs_2],[tabs_3]])

show(plt_grid)





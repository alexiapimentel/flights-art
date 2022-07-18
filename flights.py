import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import matplotlib.cm as cmx
import time
import numpy as np
import ast
import random
from pathlib import Path


def load_data() -> pd.DataFrame:
    hourly_flights = pd.read_csv('data/hourly_flights.csv')
    parse_list_cols = ['lat_origem', 'lat_destino', 'lon_origem', 'lon_destino', 'dist']
    for parse_col in parse_list_cols:
        hourly_flights[parse_col] = hourly_flights[parse_col].apply(lambda x: ast.literal_eval(x))
    hourly_flights['data_partida'] = pd.to_datetime(hourly_flights['data_partida'])
    airports = pd.read_csv('data/airports.csv')

    return hourly_flights, airports

def create_canvas(airports) -> go.Figure():
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(lon=airports['LONGEOPOINT'], lat=airports['LATGEOPOINT'], mode='markers', marker=dict(size=0.1)))
    fig.update_layout(geo=dict(scope='south america', fitbounds='locations', center=dict(lat=-13.0, lon=-53.2), showland=False, showocean=False, showcoastlines=False, showcountries=False, bgcolor='#000000'))
    fig.update_layout(paper_bgcolor = '#000000', plot_bgcolor = '#000000')
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(template='plotly_dark', showlegend=False)
    return fig

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    about, art = st.tabs(["Sobre 📘", "Flights-Art 🎨"])

    with about:
        md = Path("README.md").read_text(encoding='utf-8')
        st.markdown(md, unsafe_allow_html=True)
    
    with art:
        hourly_flights, airports = load_data()
        canvas = create_canvas(airports)
        canvas_plot = st.empty()
        previous_flight_date = hourly_flights['data_partida'][0]

        colorscales = [plt.cm.inferno, plt.cm.viridis, plt.cm.plasma, plt.cm.hot, plt.cm.Blues]
        for colorscale in colorscales:
            norm = mc.Normalize(min(hourly_flights['tot_dist']), max(hourly_flights['tot_dist']))
            colors = cmx.ScalarMappable(cmap=colorscale, norm=norm).to_rgba(hourly_flights['tot_dist'], bytes=True)
            colors = ['rgba(' + str(x[0]) + ', ' + str(x[1]) + ', ' + str(x[2]) + ', ' + str(x[3]) + ')' for x in colors]
            hourly_flights[colorscale.name] = colors
        
        for index, hf in hourly_flights.iterrows():    
            # vetorizando latitude e longitudes em uma mesma hora de partida para melhorar performance
            lons = []
            lats = []
            lons = np.empty(3 * len(hf['lon_origem']))
            lons[::3] = hf['lon_origem']
            lons[1::3] = hf['lon_destino']
            lons[2::3] = None
            lats = np.empty(3 * len(hf['lon_origem']))
            lats[::3] = hf['lat_origem']
            lats[1::3] =  hf['lat_destino']
            lats[2::3] = None
            
            current_flight_date = hf['data_partida']
            if current_flight_date != previous_flight_date:
                canvas = create_canvas(airports)
                previous_flight_date = current_flight_date
            
            # escolhendo colorscale aleatório
            choosen_scale = random.choice(colorscales)
            colors = hourly_flights[choosen_scale.name]
            canvas.add_trace(go.Scattergeo(lon=lons, lat=lats, mode='lines+markers', marker=dict(size=0.2), line=dict(color=colors[index], width=0.2), opacity=random.randrange(1, 5)/10))
            canvas_plot.plotly_chart(canvas, use_container_width=True)
            time.sleep(0.1)
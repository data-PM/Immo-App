import streamlit as st
import pandas as pd
import pickle
import numpy as np

import geopandas as gpd
import folium
from folium.features import GeoJsonPopup, GeoJsonTooltip
from streamlit_folium import st_folium
import branca



if 'liste_communes' not in st.session_state:
    st.session_state.dict_communes = pickle.load(open('./App/liste_communes_dep.p', 'rb'))
    st.session_state.liste_communes = [''] + sorted(st.session_state.dict_communes.keys())

if 'map' not in st.session_state: 
    frame = folium.Figure(width=700, height=500)
    st.session_state.map = folium.Map(location=[47.081012, 2.398782], zoom_start=6, prefer_canvas=True).add_to(frame)



APP_ICON_URL = "logo.png"

# Setup web page
st.set_page_config(
     page_title="Evolution des prix de l'immobilier",
     page_icon=APP_ICON_URL,
     layout="centered"
)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0.5rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.title("Évolution de l'immobilier à 1 an 🏡")


commune = st.selectbox(label='Choisissez votre commune', options=st.session_state.liste_communes)

if commune == '':
    st_folium(st.session_state.map, width=700, height=500)

else:

    communes = pickle.load(open('App/communes.p', 'rb'))
    lat = communes[communes.nom==commune].iloc[0]['lat']
    lon = communes[communes.nom==commune].iloc[0]['lon']

    colormap = branca.colormap.LinearColormap(
        vmin=-0.1,
        vmax=0.1,
        colors=["red", "orange", "lightblue", "green", "darkgreen"]
    )

    popup = GeoJsonPopup(
        fields=["nom", "EVOL_12M"],
        aliases=["Commune", "% Change"],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    tooltip = GeoJsonTooltip(
        fields=["nom", "EVOL_3M", "EVOL_6M", "EVOL_12M"],
        aliases=["Commune", "3 mois", "6 mois", "12 mois"],
        localize=True,
        sticky=False,
        labels=True,
        style=("background-color: white; color: #333333; font-family: arial; font-size: 14px; padding: 10px;"),
        max_width=800,
    )

    frame = folium.Figure(width=700, height=500)
    map = folium.Map(location=[lat, lon], zoom_start=11, prefer_canvas=True).add_to(frame)

    g = folium.GeoJson(
        communes,
        style_function=lambda x: {
            "fillColor": colormap(x["properties"]["evol_12m"])
            if x["properties"]["evol_12m"] is not None
            else "transparent",
            "color": "white",
            "fillOpacity": 0.4,
        },
        tooltip=tooltip,
        popup=popup,
    ).add_to(map)

    colormap.add_to(map)

    st_folium(map, width=700, height=500)



st.markdown('''
    <p><center><span style="font-size:16px">Powered by</span> <span style="font-size:20px"><strong><a href="https://dataltist.fr/" style="color:#C00000; text-decoration: none">Dataltist</a></strong></span>
    <div class="col-xs-12 col-lg-4 text-center text-sm-left"><div class="widget-theme-wrapper widget_no_background "><div id="mwt_logo_about-2" class="widget widget_logo_about"><div class="logo logo_image_only">
	<img src="//dataltist.fr/wp-content/uploads/2019/05/Logo-1.png" width="150" alt=""></center></p>
''', unsafe_allow_html=True)
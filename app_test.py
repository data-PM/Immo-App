import streamlit as st
import pandas as pd
import pickle
import numpy as np

import geopandas as gpd
import folium
from folium.features import GeoJsonPopup, GeoJsonTooltip
from shapely.geometry import Point
from streamlit_folium import st_folium
from folium import plugins
import branca



# if 'liste_communes' not in st.session_state:
    # st.session_state.dict_communes = pickle.load(open('liste_communes_dep.p', 'rb'))
    # st.session_state.liste_communes = [''] + sorted(st.session_state.dict_communes.keys())

if 'departements' not in st.session_state:
    st.session_state.departements = pickle.load(open('App/departements.p', 'rb'))  

# if 'infos_map' not in st.session_state:
#     st.session_state.infos_map = {}
#     st.session_state.infos_map['zoom'] = 6
#     st.session_state.infos_map['center'] = {}
#     st.session_state.infos_map['center']['lat'] = 47.081012
#     st.session_state.infos_map['center']['lng'] = 2.398782


# if 'zoom' not in st.session_state:
#     st.session_state.zoom = st.session_state.infos_map['zoom']

# if 'lat' not in st.session_state:
#     st.session_state.lat = st.session_state.infos_map['center']['lat']

# if 'lng' not in st.session_state:
#     st.session_state.lng = st.session_state.infos_map['center']['lng']
    


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




def update_map(zoom_level, lat, lng):

    frame = folium.Figure(width=700, height=500)
    m = folium.Map(location=[lat, lng], zoom_start=zoom_level).add_to(frame)
    plugins.Geocoder().add_to(m)

    if st.session_state.zoom >= 9:

        # departement = st.session_state.departements[st.session_state.departements.geometry.contains(Point(lng, lat))].iloc[0].nom
        
        departements = pickle.load(open('App/departements.p', 'rb'))
        departement = [departements.geometry.contains(Point(lng, lat))].iloc[0].nom


        communes = pickle.load(open('App/departements/' + departement + '.p', 'rb'))
        colormap = branca.colormap.LinearColormap(
            vmin=-0.1,
            vmax=0.1,
            colors=["red", "orange", "lightblue", "green", "darkgreen"]
        )
        folium.GeoJson(
            communes,
            style_function=lambda x: {
                "fillColor": colormap(x["properties"]["evol_12m"])
                if x["properties"]["evol_12m"] is not None
                else "transparent",
                "color": "white",
                "fillOpacity": 0.4,
            },
            # tooltip=tooltip,
            # popup=popup,
            zoom_on_click=True,
        ).add_to(m)

        colormap.add_to(m)

    return m



m = folium.Map(location=[47.081012, 2.398782], zoom_start=5)

# If you want to dynamically add or remove items from the map,
# add them to a FeatureGroup and pass it to st_folium
fg = folium.FeatureGroup(name="State bounds")
fg.add_child(
    folium.features.GeoJson(
        pickle.load(open('App/departements.p', 'rb'))
    )
)

st_folium(
    m,
    feature_group_to_add=fg,
    # center=center,
    width=700,
    height=500,
)

infos = list(st.session_state.keys())[0]
st.write(st.session_state[infos])

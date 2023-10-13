import streamlit as st
import pandas as pd
import pickle
import numpy as np

# import geopandas as gpd
import folium
from folium.features import GeoJsonPopup, GeoJsonTooltip
from streamlit_folium import st_folium
from streamlit_extras.metric_cards import style_metric_cards
import branca

from folium import FeatureGroup, LayerControl, Map, Marker

APP_ICON_URL = "logo.png"

# Setup web page
st.set_page_config(
    page_title="Evolution des prix de l'immobilier",
    page_icon=APP_ICON_URL,
    layout="centered"
)

if 'departements' not in st.session_state:
    st.session_state.departements = pickle.load(open('App/infos_dep.p', 'rb'))

# Pour enlever les espaces inutiles
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

st.title("Prix de l'immobilier à 1 an 🏡")


# Select département
list_dep = [""] + list(st.session_state.departements['dep'].unique())
dep = st.selectbox(label='Département', options=list_dep)


# Metrics
c1, c2, c3 = st.columns([1, 1, 1])

if dep == "":
    prix_0, prix_6, prix_12, evol_0, evol_6, evol_12 = "-", "-", "-", "", "", ""
else:
    prix_0 = st.session_state.departements[st.session_state.departements['dep'] == dep]['prix_figaro'].iloc[0]
    prix_6 = st.session_state.departements[st.session_state.departements['dep'] == dep]['prix_6m'].iloc[0]
    prix_12 = st.session_state.departements[st.session_state.departements['dep'] == dep]['prix_12m'].iloc[0]
    evol_0 = ""
    evol_6 = st.session_state.departements[st.session_state.departements['dep'] == dep]['EVOL_6M'].iloc[0]
    evol_12 = st.session_state.departements[st.session_state.departements['dep'] == dep]['EVOL_12M'].iloc[0]

background_color: str = '#FFF'
border_size_px: int = 1
border_color: str = '#CCC'
border_radius_px: int = 5
border_left_color: str = '#9AD8E1'

st.markdown(
    f"""
    <style>
        div[data-testid="metric-container"] {{
            background-color: {background_color};
            border: {border_size_px}px solid {border_color};
            padding: 5% 5% 5% 10%;
            border-radius: {border_radius_px}px;
            border-left: 0.5rem solid {border_left_color} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

c1.metric("Aujourd'hui", prix_0, evol_0)
c2.metric("Dans 6 mois", prix_6, evol_6)
c3.metric("Dans 1 an", prix_12, evol_12)



# Map

if dep == "":
    frame = folium.Figure(width=800, height=500)
    map = folium.Map(tiles="openstreetmap", location=[47.081012, 2.398782], zoom_start=6, max_bounds=True).add_to(frame)

else:
    lat = st.session_state.departements[st.session_state.departements['dep'] == dep]['lat'].iloc[0]
    lng = st.session_state.departements[st.session_state.departements['dep'] == dep]['lng'].iloc[0]
    zoom = st.session_state.departements[st.session_state.departements['dep'] == dep]['zoom'].iloc[0]

    frame = folium.Figure(width=800, height=500)
    map = folium.Map(tiles="openstreetmap", location=[lat, lng], zoom_start=zoom).add_to(frame)

    dep_light = dep[5:]
    communes = pickle.load(open('App/departements/' + dep_light + '.p', 'rb'))
    communes['rien'] = ""

    #Create the choropleth map add it to the base map
    custom_scale = (communes['evol_12m'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()

    colormap = branca.colormap.LinearColormap(
        vmin=-0.1,
        vmax=0.1,
        colors=["red", "orange", "lightblue", "green", "darkgreen"]
    )
    folium.Choropleth(
        geo_data=communes,
        data=communes,
        columns=['code', 'evol_12m'],  #Here we tell folium to get the county fips and plot new_cases_7days metric for each county
        key_on='feature.properties.code', #Here we grab the geometries/county boundaries from the geojson file using the key 'coty_code' which is the same as county fips
        # threshold_scale=[i/50 for i in range(-5, 5)], #use the custom scale we created for legend
        # fill_color='RdYlGn',
        nan_fill_color="White", #Use white color if there is no data available for the county
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Variation du prix au m²', #title of the legend
        highlight=True,
        line_color='black').add_to(map)
    
    # colormap.add_to(map)



    #Add Customized Tooltips to the map
    folium.features.GeoJson(
        data=communes,
        name='New Cases Past 7 days (Per 100K Population)',
        smooth_factor=2,
        style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
        zoom_on_click=True,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['nom',
                    'rien',
                    'prix_figaro',
                    'rien',
                    'prix_6m',
                    'EVOL_6M',
                    'rien',
                    'prix_12m',
                    'EVOL_12M'
                    ],
            aliases=["Commune ",
                     "---------------------------",
                     "Prix du m² ",
                     "---------------------------",
                     "Prix dans 6 mois ",
                     " ",
                     "---------------------------",
                     "Prix dans 1 an ",
                     " ",
                    ], 
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,),
                highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
            ).add_to(map)

    
st_folium(map, width=800, height=500)


# Dataltist
st.markdown('''
    <p><center><span style="font-size:16px">Powered by</span> <span style="font-size:20px"><strong><a href="https://dataltist.fr/" style="color:#C00000; text-decoration: none">Dataltist</a></strong></span>
    <div class="col-xs-12 col-lg-4 text-center text-sm-left"><div class="widget-theme-wrapper widget_no_background "><div id="mwt_logo_about-2" class="widget widget_logo_about"><div class="logo logo_image_only">
    <img src="//dataltist.fr/wp-content/uploads/2019/05/Logo-1.png" width="150" alt=""></center></p>
''', unsafe_allow_html=True)
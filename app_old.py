import streamlit as st
import pandas as pd
import pickle
import numpy as np
import pydeck as pdk


if 'df' not in st.session_state:
    st.session_state.df = pickle.load(open('./App/liste_res_20231002.p', 'rb'))
    st.session_state.df.index = st.session_state.df.nom
    st.session_state.liste_commune = [''] + sorted(st.session_state.df.nom.unique())

if 'lat' not in st.session_state:
    st.session_state.lat = 47.081012
    st.session_state.lon = 2.398782
    st.session_state.zoom = 5
    st.session_state.max_range = float(st.session_state.df['evol_12m'].max())
    st.session_state.min_range = float(st.session_state.df['evol_12m'].min())



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


commune = st.selectbox(label='Choisissez votre commune', options=st.session_state.liste_commune)

if commune != '':
    EVOL_3M = st.session_state.df.loc[commune, 'EVOL_3M']
    EVOL_6M = st.session_state.df.loc[commune, 'EVOL_6M']
    EVOL_12M = st.session_state.df.loc[commune, 'EVOL_12M']
    st.session_state.lat = st.session_state.df.loc[commune, 'lat']
    st.session_state.lon = st.session_state.df.loc[commune, 'lon']
    st.session_state.zoom = 11

st.pydeck_chart(pdk.Deck(
    map_style='light',
    initial_view_state=pdk.ViewState(
        latitude=st.session_state.lat,
        longitude=st.session_state.lon,
        zoom=st.session_state.zoom,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ColumnLayer',
            data=st.session_state.df,
            get_position='[lon, lat]',
            get_elevation = 'evol_12m',
            radius=500,
            elevation_scale=500,
            get_fill_color='evol_12m*10000',
            auto_highlight=True,
            pickable=True,
            extruded=True,
        ),
    ],
    tooltip = {
        "html": "<b>{nom}</b><br>3 mois : <b>{EVOL_3M}</b><br>6 mois : <b>{EVOL_6M}</b><br>12 mois : <b>{EVOL_12M}</b>",
        "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }
))

st.markdown('''
    <p><center><span style="font-size:16px">Powered by</span> <span style="font-size:20px"><strong><a href="https://dataltist.fr/" style="color:#C00000; text-decoration: none">Dataltist</a></strong></span>
    <div class="col-xs-12 col-lg-4 text-center text-sm-left"><div class="widget-theme-wrapper widget_no_background "><div id="mwt_logo_about-2" class="widget widget_logo_about"><div class="logo logo_image_only">
	<img src="//dataltist.fr/wp-content/uploads/2019/05/Logo-1.png" width="150" alt=""></center></p>
''', unsafe_allow_html=True)
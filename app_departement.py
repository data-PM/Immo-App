import streamlit as st
import pandas as pd
import pickle
import numpy as np

# import geopandas as gpd
import folium
from folium.features import GeoJsonPopup, GeoJsonTooltip
from streamlit_folium import st_folium
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid
import branca
from streamlit_js_eval import streamlit_js_eval



from folium import FeatureGroup, LayerControl, Map, Marker

APP_ICON_URL = "logo.png"

# Setup web page
st.set_page_config(
    page_title="Evolution des prix de l'immobilier",
    page_icon=APP_ICON_URL,
    layout="wide"
)

if 'dep' not in st.session_state:
    st.session_state.dep = ""

if 'com' not in st.session_state:
    st.session_state.com = ""

if 'index_com' not in st.session_state:
    st.session_state.index_com = 0
    
if 'france' not in st.session_state:
    st.session_state.france = pickle.load(open('france.p', 'rb'))

if 'departements' not in st.session_state:
    st.session_state.departements = pickle.load(open('infos_dep.p', 'rb'))
    st.session_state.departements['dep'] = st.session_state.departements['dep'].apply(lambda x: str(x).split(' - ')[1])
    
if 'communes' not in st.session_state:
    st.session_state.communes = pickle.load(open('communes.p', 'rb'))

if 'communes_dict' not in st.session_state:
    st.session_state.communes_dict = pickle.load(open('liste_communes_dep.p', 'rb'))

if 'communes_list' not in st.session_state:
    st.session_state.communes_list = sorted(list(st.session_state.communes_dict.keys()))







# if 'mobile' not in st.session_state:
#     if streamlit_js_eval(js_expressions='screen.width', key = 'SCR') < 600:
#         st.session_state.mobile = True
#     else:
#         st.session_state.mobile = False

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

# if st.session_state.mobile:
#     st.markdown("<h3 style='text-align: center;'>💸 Prix de l'immobilier à <span style='color: #bd4937'>1 an</span> 💸</h3>", unsafe_allow_html=True)
# else:
#     st.markdown("<h1 style='text-align: center;'>💸 Prix de l'immobilier à <span style='color: #bd4937'>1 an</span> 💸</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>💸 Prix de l'immobilier à <span style='color: #bd4937'>1 an</span> 💸</h1>", unsafe_allow_html=True)


# try:
#     if st.session_state.map['last_active_drawing'] is not None:
#         st.success(st.session_state.map['last_active_drawing']['properties']['nom'])
# except:
#     st.error('rien')


_, c1, c2, _ = st.columns([1, 4, 6, 1])


with c1:

    # mise en forme Metrics
    background_color: str = '#FFF'
    border_size_px: int = 1
    border_color: str = '#CCC'
    border_radius_px: int = 5
    border_left_color: str = '#bd4937'

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


    my_grid = grid([1, 1], 3, 1, 3, 1, 3, vertical_align="bottom")

    # Select commune
    list_commune = [""] + st.session_state.communes_list
    st.session_state.com = my_grid.selectbox(label='Commune', options=list_commune, index=st.session_state.index_com)
    my_grid.write('')


    # Communes
    if st.session_state.com == "":
        prix_0, prix_6, prix_12, evol_0, evol_6, evol_12 = "-", "-", "-", "", "", ""
        dep = ""
    else:
        dep = st.session_state.communes_dict[st.session_state.com]
        prix_0 = st.session_state.communes[st.session_state.communes['nom'] == st.session_state.com]['prix_figaro'].iloc[0]
        prix_6 = st.session_state.communes[st.session_state.communes['nom'] == st.session_state.com]['prix_6m'].iloc[0]
        prix_12 = st.session_state.communes[st.session_state.communes['nom'] == st.session_state.com]['prix_12m'].iloc[0]
        evol_0 = "0"
        evol_6 = st.session_state.communes[st.session_state.communes['nom'] == st.session_state.com]['EVOL_6M'].iloc[0]
        evol_12 = st.session_state.communes[st.session_state.communes['nom'] == st.session_state.com]['EVOL_12M'].iloc[0]

    my_grid.metric("Aujourd'hui", prix_0, evol_0)
    my_grid.metric("Dans 6 mois", prix_6, evol_6)
    my_grid.metric("Dans 1 an", prix_12, evol_12)



    # Département

    # Select département
    # list_commune = [""] + st.session_state.communes_list
    # st.session_state.com = my_grid.selectbox(label='Commune', options=list_commune, index=st.session_state.index_com)
    list_dep = [""] + list(st.session_state.departements['dep'].unique())

    # def update_commune():
    #     st.session_state.index_com = 0
    #     st.session_state.com = ""
    #     st.rerun()
    
    # st.session_state.dep = my_grid.selectbox(label='Département', options=list_dep, index=list_dep.index(dep), on_change=update_commune)
    # my_grid.write("")

    titre_dep = my_grid.empty()
    if st.session_state.com == "":
        titre_dep.markdown('''<h6>Département</h6>''', unsafe_allow_html=True)
        prix_dep_0, prix_dep_6, prix_dep_12, evol_dep_0, evol_dep_6, evol_dep_12 = "-", "-", "-", "", "", ""
    else:
        # titre_dep.write(dep)
        titre_dep.markdown('<h6>'+dep+'</h6>', unsafe_allow_html=True)
        prix_dep_0 = st.session_state.departements[st.session_state.departements['dep'] == dep]['prix_figaro'].iloc[0]
        prix_dep_6 = st.session_state.departements[st.session_state.departements['dep'] == dep]['prix_6m'].iloc[0]
        prix_dep_12 = st.session_state.departements[st.session_state.departements['dep'] == dep]['prix_12m'].iloc[0]
        evol_dep_0 = "0"
        evol_dep_6 = st.session_state.departements[st.session_state.departements['dep'] == dep]['EVOL_6M'].iloc[0]
        evol_dep_12 = st.session_state.departements[st.session_state.departements['dep'] == dep]['EVOL_12M'].iloc[0]

    my_grid.metric("Aujourd'hui", prix_dep_0, evol_dep_0)
    my_grid.metric("Dans 6 mois", prix_dep_6, evol_dep_6)
    my_grid.metric("Dans 1 an", prix_dep_12, evol_dep_12)


    # France entière
    my_grid.markdown('''<h6>France entière</h6>''', unsafe_allow_html=True)
    my_grid.metric("Aujourd'hui", st.session_state.france['prix_figaro'], '0')
    my_grid.metric("Dans 6 mois", st.session_state.france['prix_6m'], st.session_state.france['evol_6m'])
    my_grid.metric("Dans 1 an", st.session_state.france['prix_12m'], st.session_state.france['evol_12m'])










with c2:
        
    # Map
    if dep == "":

        frame = folium.Figure(width=900, height=600)
        map = folium.Map(tiles="openstreetmap", location=[47.081012, 2.398782], zoom_start=6, max_bounds=True).add_to(frame)

    else:
        
        lat = st.session_state.departements[st.session_state.departements['dep'] == dep]['lat'].iloc[0]
        lng = st.session_state.departements[st.session_state.departements['dep'] == dep]['lng'].iloc[0]
        zoom = st.session_state.departements[st.session_state.departements['dep'] == dep]['zoom'].iloc[0]

        frame = folium.Figure(width=900, height=600)
        map = folium.Map(tiles="openstreetmap", location=[lat, lng], zoom_start=zoom).add_to(frame)

        if dep[0].isnumeric():
            dep_light = dep[5:]
        else:
            dep_light = dep
        communes = pickle.load(open('departements/' + dep_light + '.p', 'rb'))
        communes['rien'] = "-------------"

        colormap = branca.colormap.LinearColormap(
            vmin=-0.1,
            vmax=0.1,
            colors=["red", "orange", "lightblue", "green", "darkgreen"]
        )

        folium.GeoJson(
            communes,
            style_function=lambda x: {
                "fillColor": colormap(x["properties"]["evol_12m_lisse"])
                if x["properties"]["evol_12m_lisse"] is not None
                else "transparent",
                "color": "#333333",
                "weight": 0.1,
                "fillOpacity": 0.4,
                'lineColor': '#333333',
            }
        ).add_to(map)

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
                        'evol_12m_lisse'
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
                sticky=True,
                labels=True,
                style="""
                    background-color: #F0EFEF;
                    border: 2px solid black;
                    border-radius: 3px;
                    box-shadow: 3px;
                """,
                max_width=900,),
                    highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                ).add_to(map)


        colormap.add_to(map)

        
    st.session_state.map = st_folium(map, width=900, height=600)

# if st.session_state.map['last_active_drawing'] is not None:
#     st.success(st.session_state.map['last_active_drawing']['properties']['nom'])
# else:
#     st.error('rien')

# if st.session_state.map['last_active_drawing'] is not None:
#     clicked_commune = st.session_state.map['last_active_drawing']['properties']['nom']
#     st.session_state.index_com = list_commune.index(clicked_commune)
#     st.write('')
#     # st.session_state.com = clicked_commune
#     # st.write(st.session_state.index_com)
#     # st.rerun()



# Dataltist
st.markdown('''
    <center><span style="font-size:16px">created by</span> <a href="https://dataltist.fr/" style="color:#C00000; text-decoration: none">
    <div class="col-xs-12 col-lg-4 text-center text-sm-left"><div class="widget-theme-wrapper widget_no_background "><div id="mwt_logo_about-2" class="widget widget_logo_about"><div class="logo logo_image_only">
    <img src="https://dataltist.fr/wp-content/uploads/2023/09/Logo-light-dataltist-Forsides.png" width="150" alt=""></a></span></center>
''', unsafe_allow_html=True)

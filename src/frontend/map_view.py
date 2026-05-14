import pydeck as pdk
import pandas as pd
import streamlit as st

def render_map(df: pd.DataFrame):
    if df.empty: return

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=11, pitch=45
    )
    
    layer = pdk.Layer(
        "ScatterplotLayer", data=df,
        get_position="[lon, lat]", 
        get_color="color",
        get_radius=100,
        radius_min_pixels=6,     
        radius_max_pixels=15,      
        pickable=True
    )
    
    st.pydeck_chart(pdk.Deck(
        map_style="dark",
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"text": "Locker: {Name}\nScore: {Score}\n{Reasoning}"}
    ))
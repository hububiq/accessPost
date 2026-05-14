import pandas as pd
import json, os
import streamlit as st

# streamlit reruns app.py everytime and would try to load data,colours over again with every slide on browser. therefore cache is used

@st.cache_data
def load_processed_data() -> pd.DataFrame: #pandas dataframe returned
    filepath = os.path.join("data", "lockers_warszawa_scored.json")
    if not os.path.exists(filepath): return pd.DataFrame()
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    data = []
    colors = {
        5: [0, 255, 0, 200],      # Green
        4: [0, 255, 0, 200],      # Green
        3: [255, 165, 0, 200],    # Orange
        2: [255, 0, 0, 200],      # Red
        1: [255, 0, 0, 200],      # Red
        0: [0, 150, 255, 160]     # Blue (No Data / No Image)
    }
              
    for l in raw_data:
        score = l.get('accessibility_score') or 0
        
        lat = float(l.get('location', {}).get('latitude', 0))
        lon = float(l.get('location', {}).get('longitude', 0))
        
        # Only add to map if we actually have valid GPS coordinates
        if lat != 0 and lon != 0:
            data.append({
                "Name": l.get('name'),
                "Score": score,
                "Reasoning": l.get('accessibility_reasoning', 'No data'),
                "lat": lat,
                "lon": lon,
                "color": colors.get(score, [0, 150, 255, 160])
            })
            
    return pd.DataFrame(data)
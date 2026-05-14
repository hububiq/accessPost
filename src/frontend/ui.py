import streamlit as st
import pandas as pd

def setup_header():
    st.set_page_config(page_title="AccessiPost", page_icon="♿", layout="wide")
    st.title("♿ accessPost")
    st.subheader("AI-Powered Accessibility Audit for InPost Lockers")
    st.markdown("🟢 Good (4-5) | 🟠 Moderate (3) | 🔴 Poor (1-2) | 🔵 No Data (0)")

def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filter Lockers")
    st.sidebar.markdown("**Data Summary:**")
    st.sidebar.dataframe(df['Score'].value_counts().rename_axis('Score').reset_index(name='Count'), hide_index=True)
    st.sidebar.divider()
    selected = st.sidebar.multiselect(
        "Select Accessibility Scores:",
        options=[5, 4, 3, 2, 1, 0], default=[5, 4, 3, 2, 1, 0],
        format_func=lambda x: f"Score {x}" if x > 0 else "No Data"
    )
    return df[df['Score'].isin(selected)]

def render_data_table(df: pd.DataFrame):
    st.divider()
    st.subheader("Raw Audit Data")
    clean_df = df.drop(columns=['color', 'lat', 'lon'], errors='ignore')
    st.dataframe(clean_df, use_container_width=True)
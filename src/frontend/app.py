import streamlit as st
from data_loader import load_processed_data
from ui import setup_header, render_sidebar_filters, render_data_table
from map_view import render_map

def main():
    # 1. Setup Page & Headers
    setup_header()

    # 2. Load Data
    df = load_processed_data()
    if df.empty:
        st.error("No data found. Run the backend pipeline first")
        return

    # 3. Apply Filters
    filtered_df = render_sidebar_filters(df)
    st.markdown(f"**Showing {len(filtered_df)} lockers based on your filters**")

    # 4. Render Components
    render_map(filtered_df)

    unique_locations = len(filtered_df.drop_duplicates(subset=['lat', 'lon']))
    st.warning(f"🕵️ Debug: Out of {len(filtered_df)} lockers, there are only {unique_locations} UNIQUE map coordinates!")

    render_data_table(filtered_df)

if __name__ == "__main__":
    main()
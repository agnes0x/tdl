# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.io as pio
import data

#Local variables (for querying!)

st.header("Please enter your address, we'll fetch governance forums relevant to your holdings ")

address = st.text_input("Please enter your address:", value="0xE831C8903de820137c13681E78A5780afDdf7697", max_chars=42 )

#-----------------------------------------
# Global Variables (keep template clean, no changes beyond this point)!
theme_plotly = None # None or streamlit

# Config
st.set_page_config(page_title='Deep dive:' +protocol_name, page_icon=':bar_chart:', layout='wide')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
# Data Sources
data_gov = get_data_governance()

filterlist_s = get_data_wallet(address)

filtered_df = get_filtered_gov(data_gov, filterlist_s)

# Process Data

st.write("Here are the forum posts that affect your portfolio")


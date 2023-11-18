# Libraries
import streamlit as st
from PIL import Image

# Confit
st.set_page_config(page_title='DAO ', page_icon= '👻', layout='wide')

# Title
st.title('Governance Forum monitoring tool')

# Content
c1, c2 = st.columns(2)
c1.image(Image.open('images/aave2.png'))

#with Image.open(file_path) as img:
#   c1.image(img)


st.write(
    """
    This tool is designed to empower Aave ecosystem participants to effortlessly filter & track relevant activity on Aave governance forums, based on the user's wallet activity.
    This tool is designed and structured in multiple **Pages** that are accessible using the sidebar.
    Each of these Pages addresses a different functionality.
    """
)

st.subheader('Methodology')
st.write(
    """
    The data for this forum activity monitoring tool were scraped from the [**Aave governance forum**](https://https://governance.aave.com/) & pulled from Etherscan using its **API**.
    These queries are currently called to re-run when accessing a Page, and are imported as a JSON file directly to each page - be patient.
    
    From governance forum, currently we use:
    Title of posts
    
    From wallets, currently we use:
    Historical interactions with ERC20 tokens
    
    """
)

st.subheader('Future Works')
st.write(
    """
    This tool is a work in progress and will continue to be developed moving forward. Adding better-suited wallet position APIs (Zerion, Zapper) to pull only current data,
    as well as better filtering. Feel free to share your feedback, suggestions, and
    also critics with me.
    """
)

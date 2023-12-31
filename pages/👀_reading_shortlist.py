# Libraries
import streamlit as st
import pandas
import plotly.express as px
import numpy 
import requests 
import time

#Local variables (for querying!)

# Config
st.set_page_config(page_title='Shortlist gov posts', page_icon='👀', layout='wide')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

st.header(" 👀 Shortlist of governance posts affecting you! 👀 ")

address = st.text_input("Please enter your address & press enter", value="0xE831C8903de820137c13681E78A5780afDdf7697", max_chars=42 )

#-----------------------------------------
# Global Variables (keep template clean, no changes beyond this point)!
theme_plotly = None # None or streamlit


# Data functions
def get_data_governance():
    # base URL
    base_url = "https://governance.aave.com/c/governance/4/l/latest.json?filter=default&page="

    #Page count 
    page_count = 1

    query1 = f"{base_url}{page_count}"

    #df to hold data 
    #response = requests.get(query).json()

    #list to hold data
    data_gov = []

    # Infinite loop, will break when no next page is available
    while True:
    
        # Construct the URL for the current page
        query1 = f"{base_url}{page_count}"

        # Send a request to the current URL
        response = requests.get(query1)
    
        # Check if the response is successful
        if response.status_code == 200:
            try:   
                # Process and add the data to the list
                df = requests.get(query1).json()
                data_gov.extend(df["topic_list"]["topics"])
        
                # Check if there is a next page
                if not df["topic_list"]["more_topics_url"]:
                    break
        
                # Increment the page count for the next iteration
                page_count += 1
        
                #rate limit
                time.sleep(2)
        
            except KeyError:
                # Break the loop if 'more_topics_url' key is not found
                break        
        else:
            print(f"Failed to fetch data from {query1}")
            break

    # Convert the list to a DataFrame
    data_gov = pandas.json_normalize(data_gov)

    # complete slug urls
    topic_url = "https://governance.aave.com/t/"
    data_gov['link'] = topic_url + data_gov['slug']

    data_gov = data_gov[['title','created_at','link']]

    # Save the DataFrame to a file, e.g., CSV
    #data.to_csv('govforum_data.csv', index=False)
    return data_gov


#ideally would call zerion or zapper api to get current token balances & wallet positions, but sadly haven't got an api key on hand :(
#placeholder version with etherscan

def get_data_wallet(address):
    # Set wallet address

    # Etherscan api url
    url1 = 'https://api.etherscan.io/api?module=account&action=tokentx&address='

    url2 = "&page=1&offset=1000&startblock=0&endblock=27025780&sort=asc&apikey="

    api_key = st.secrets["my_cool_secrets"]["etherscan_api_key"]

    query = url1 + address + url2 + api_key 

    # Get data
    response2 = requests.get(query).json()
    df = pandas.json_normalize(response2['result'])

    # set filter data

    # get list of tokens historically interacted with
    filterlist_s = list(set(df['tokenSymbol']))
    filterlist_s.remove('AAVE')

    # determine if lender or borrower

    lender = False

    borrower = False

    filterlist_name = list(set(df['tokenName']))

    for item in filterlist_name:
        if 'Aave interest bearing ' in item:
            lender = True
            filterlist_s.extend(['borrow'])
            break  # Stop searching once a match is found

    for item in filterlist_name:
        if 'Aave variable debt bearing ' in item:
            borrower = True
            filterlist_s.extend(['lend'])
            break  # Stop searching once a match is found        

    return filterlist_s


# Filter DataFrame based on whether the value in filterlist is also in column_name
def get_filtered_gov(data_gov, filterlist_s):

    filtered_df = data_gov[data_gov['title'].apply(lambda title: any(word in title for word in filterlist_s))]
    #filtered_df = data[data['title'].apply(lambda title: any(word == title for word in filterlist_s))]

    return filtered_df

#def make_clickable(val):
    # target _blank to open new window
    #return f'<a target="_blank" href="{val}">{val}</a>'



# Data Sources
st.write("Please remain patient")

data_gov = get_data_governance()

filterlist_s = get_data_wallet(address)

filtered_df = get_filtered_gov(data_gov, filterlist_s)

#filtered_df = filtered_df.style.format({'link': make_clickable})

# Process Data

st.write("Here are the forum posts that affect your portfolio")

st.write(filtered_df)





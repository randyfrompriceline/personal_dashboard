
from datetime import date, datetime
from numpy import power
import numpy as np
from typing import final
import streamlit as st
import pandas as pd
import seaborn as sns
import functools
import json

streamlit_data = pd.read_csv('streamlitdata.csv')

st.table(data=streamlit_data)

brand_owner_chosen = st.sidebar.multiselect('Brand Owner Name', streamlit_data['Brand_Owner_Name'].unique())
country_chosen = st.sidebar.multiselect('Hotel Country Name',streamlit_data['Hotel_Country_Name'].unique())
state_chosen = st.sidebar.multiselect('Hotel State Name',streamlit_data['Hotel_State_Name'].unique())
metro_chosen = st.sidebar.multiselect('Metro Region Name',streamlit_data['Metro_Region_Name'].unique())
week_chosen = st.sidebar.multiselect('Week',streamlit_data['Week_Num'].unique())

attribute_selection = st.sidebar.multiselect('Attribute Selection', list(streamlit_data.columns))
        
selections = [brand_owner_chosen,country_chosen,state_chosen,metro_chosen,week_chosen]


if country_chosen in ("", []):
    		country_filter = streamlit_data['Hotel_Country_Name'].unique()
else:
    country_filter = country_chosen

if brand_owner_chosen in ("", []):
    		brand_filter = streamlit_data['Brand_Owner_Name'].unique()
else:
    brand_filter = brand_owner_chosen


filtered = streamlit_data[(streamlit_data['Brand_Owner_Name'].isin(brand_filter) & (streamlit_data['Hotel_Country_Name'].isin(country_filter)))]

st.write(filtered)

def percent_out_of_total(attribute):
    if attribute in ("",[]):
        attribute = 'Week_Num'
        rmnts_gb = filtered.groupby(attribute,as_index=False)['RMNTS'].sum()
        st.write(rmnts_gb) 
    else:
        chosen_total = filtered.groupby(attribute,as_index=False)['RMNTS'].sum()
        chosen_total['Total'] = chosen_total['RMNTS'].sum().astype(float).round(1)
        chosen_total['Percent_Out_Of_Total'] = (100 * ((chosen_total['RMNTS'] / chosen_total['Total']))).astype(float).round(1)
        chosen_total.reset_index(drop=True)
        sorted_total = chosen_total.sort_values(by='RMNTS', ascending=False)
        st.write(sorted_total)

percent_out_of_total(attribute_selection)

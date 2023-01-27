
from datetime import date, datetime
from numpy import power
import numpy as np
from typing import final
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from  matplotlib.ticker import FuncFormatter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import json

import streamlit as st

streamlit_data = pd.read_csv(r'C:\Users\rrichardson\Downloads\streamlitdata.csv')

st.sidebar.write('Select Attributes to Filter By:')
attribute_selection = st.sidebar.multiselect('Attribute Selection', options=list(streamlit_data.columns))
chosen_sum = st.sidebar.multiselect('Chosen Sum', ['sum','avg','max','min'])


st.sidebar.write('')

st.sidebar.write('Filter by Brand Owner, Country, State, Metro Region, and Week:')
brand_owner_chosen = st.sidebar.multiselect('Brand Owner Name', streamlit_data['Brand_Owner_Name'].unique())
country_chosen = st.sidebar.multiselect('Hotel Country Name',streamlit_data['Hotel_Country_Name'].unique())
state_chosen = st.sidebar.multiselect('Hotel State Name',streamlit_data['Hotel_State_Name'].unique())
metro_chosen = st.sidebar.multiselect('Metro Region Name',streamlit_data['Metro_Region_Name'].unique())
week_chosen = st.sidebar.multiselect('Week',streamlit_data['Week_Num'].unique())



# selections = [brand_owner_chosen,country_chosen,state_chosen,metro_chosen,week_chosen]


# def groupbys(data):
#    for n in range(-1,7):
#        n == 0
#        columns = data.iloc[:,[n+1,7]]
#        if columns.iloc[:,0].tolist() == 'Week_Num':
#            data = columns.groupby(columns.iloc[:,0]).sum('RMNTS')
#        else:
#            data = columns.groupby(columns.iloc[:,0]).sum('RMNTS').sort_values(by='RMNTS',ascending=False)
#        st.table(data)   
#        if n == 7:
#            break
# groupbys(streamlit_data)

# if attribute_selection in ("", []):
#     attribute_filter = list(streamlit_data.columns)
# else:
#     attribute_filter = attribute_selection

if country_chosen in ("", []):
    country_filter = streamlit_data['Hotel_Country_Name'].unique()
else:
    country_filter = country_chosen

if brand_owner_chosen in ("", []):
    brand_filter = streamlit_data['Brand_Owner_Name'].unique()
else:
    brand_filter = brand_owner_chosen

if state_chosen in ("", []):
    state_filter = streamlit_data['Hotel_State_Name'].unique()
else:
    state_filter = state_chosen

if metro_chosen in ("", []):
    metro_filter = streamlit_data['Metro_Region_Name'].unique()
else:
    metro_filter = metro_chosen

if week_chosen in ("", []):
    week_filter = streamlit_data['Week_Num'].unique()
else:
    week_filter = week_chosen

filtered = streamlit_data[(streamlit_data['Brand_Owner_Name'].isin(brand_filter) & (streamlit_data['Hotel_Country_Name'].isin(country_filter)))]

st.dataframe(filtered)

dataframe = filtered
love = attribute_selection


# # created_list = attribute_filter.unique().tolist()
# filtered_dict = {}

# for kind in love:
#     filtered_dict[kind] = dataframe[dataframe[love] == kind]

def analysis():
#   for key, value in filtered_dict.items():
    agg_func_math = {
    'RMNTS':
    ['sum', 'mean', 'median', 'min', 'max', 'std', 'var', 'count']
    }
    groupby = dataframe.groupby(love,as_index=False).agg(agg_func_math)

    st.write("",groupby)

analysis()


# def percent_out_of_total(attribute):
#     if attribute in ("",[]):
#         attribute = 'Week_Num'
#         rmnts_gb = filtered.groupby(attribute,as_index=False)['RMNTS'].sum()
#         st.write(rmnts_gb) 
#     else:
#         chosen_total = filtered.groupby(attribute,as_index=False)['RMNTS'].sum()
#         chosen_total['Total'] = chosen_total['RMNTS'].sum().astype(float).round(1)
#         chosen_total['Percent_Out_Of_Total'] = (100 * ((chosen_total['RMNTS'] / chosen_total['Total']))).astype(float).round(1)
#         chosen_total.reset_index(drop=True)
#         sorted_total = chosen_total.sort_values(by='RMNTS', ascending=False)
#         st.write(sorted_total)

# percent_out_of_total(attribute_selection)





# dataframe = filtered
# filter_by = 'Brand_Owner_Name'

# created_list = dataframe[filter_by].unique().tolist()
# filtered_dict = {}

# for kind in created_list:
#     filtered_dict[kind] = dataframe[dataframe[filter_by] == kind]

# def analysis():
#   for key, value in filtered_dict.items():
#     rmnts = filtered_dict[key][['RMNTS','RMNTS_PY']].corr()

#     st.write("",key,rmnts)

# analysis()


# st.write(dataframe)
# filter_by = 'Brand_Owner_Name'

# xaxis = 'Week_Num'
# newdataframe = dataframe.groupby(['Week_Num','Brand_Owner_Name'],as_index=False).agg({'RMNTS':'sum','RMNTS_PY':'sum'})

# created_list = newdataframe[filter_by].unique().tolist()
# filtered_dict = {}

# for kind in created_list:
#     filtered_dict[kind] = newdataframe[newdataframe[filter_by] == kind]

# def analysis():
#   for key, value in filtered_dict.items():
#     fig = make_subplots(specs=[[{"secondary_y": True}]],)


#     fig.add_trace(
#     go.Scatter(x=filtered_dict[key][xaxis], y=filtered_dict[key]['RMNTS'], name="RMNTS"),
#     secondary_y=False, 
#     )

#     fig.add_trace(
#         go.Scatter(x=filtered_dict[key][xaxis], y=filtered_dict[key]['RMNTS_PY'], name="RMNTS_PY"),
#         secondary_y=False,
#     )

#     fig.update_xaxes(title_text="Week_Num",tickformat="%q\n%Y",fixedrange=True,matches=None)
#     fig.update_layout(title=key,width=900,height=400)
#     fig.update_yaxes(rangemode="tozero")


#     st.plotly_chart(fig, use_container_width=True)


# analysis()

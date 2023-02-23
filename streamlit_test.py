
from datetime import date, datetime
import datetime
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
import os
import openai
import streamlit as st
import db_dtypes




today = datetime.datetime.today()
start_week = today - datetime.timedelta(days=today.weekday() + 1)
start_week = start_week - datetime.timedelta(days=7)
end_week = start_week + datetime.timedelta(days=6)
# return (start_week, end_week)

# prev_week_range()

# start, end = prev_week_range()
# week_start = start.strftime('%Y-%m-%d')
# week_end = end.strftime('%Y-%m-%d')


# streamlit_data = pd.read_csv(r'C:\Users\rrichardson\Downloads\streamlitdata.csv')
streamlit_data = pd.read_pickle(r'C:\Users\rrichardson\Downloads\pcln_data (2).pkl')
# st.dataframe(streamlit_data)

list_attributes= streamlit_data.columns[[0,1,2]].tolist()
attribute_selection = st.sidebar.multiselect('Attribute Selection', options=list_attributes)


st.sidebar.write('')

st.sidebar.write('Filters:')
date_begin_chosen = st.sidebar.date_input('Date Beginning', start_week,max_value=end_week)
date_end_chosen = st.sidebar.date_input('Date Ending', end_week)
brand_owner_chosen = st.sidebar.multiselect('Brand Owner Name', streamlit_data['BRAND_NAME'].unique())
country_chosen = st.sidebar.multiselect('Hotel Country Name',streamlit_data['HOTEL_COUNTRY_NAME'].unique())



top_metro_check = st.sidebar.checkbox('Top 20 Metros')

if top_metro_check:
    sorted_metros = streamlit_data.groupby('METRO_REGION_NAME')['RMNTS_CY'].sum().reset_index().sort_values(by='RMNTS_CY',ascending=False)
    top_20_metros = sorted_metros['METRO_REGION_NAME'].head(20).to_list()
    all_metros_filtered = streamlit_data['METRO_REGION_NAME'].unique().isin(top_20_metros).to_list()
    metro_chosen = st.sidebar.multiselect('Metro Region Name',all_metros_filtered)
    metro_filter = metro_chosen
elif not top_metro_check:
    metro_chosen = st.sidebar.multiselect('Metro Region Name',streamlit_data['METRO_REGION_NAME'].unique())
    top_20_metros = streamlit_data['METRO_REGION_NAME'].unique()
    metro_filter = metro_chosen


week_chosen = st.sidebar.multiselect('Week',streamlit_data['WEEK_BEGIN_DATE'].sort_values(ascending=True).unique())
# top_metro_check = st.sidebar.checkbox('Top 20 Metros')

# if top_metro_check:
#     sorted_metros = streamlit_data.groupby('METRO_REGION_NAME')['RMNTS_CY'].sum().reset_index().sort_values(by='RMNTS_CY',ascending=False)
#     top_20_metros = sorted_metros['METRO_REGION_NAME'].head(20).to_list()
# else:
#     top_20_metros = streamlit_data['METRO_REGION_NAME'].unique()   

# if top_metro_check:
#     metro_chosen = streamlit_data['METRO_REGION_NAME'].isin(top_20_metros).unique()
# else:
#     metro_filter = metro_chosen

if country_chosen in ("", []):
    country_filter = streamlit_data['HOTEL_COUNTRY_NAME'].unique()
else:
    country_filter = country_chosen

if brand_owner_chosen in ("", []):
    brand_filter = streamlit_data['BRAND_NAME'].unique()
else:
    brand_filter = brand_owner_chosen

if week_chosen in ("", []):
    week_filter = streamlit_data['WEEK_BEGIN_DATE'].unique()
else:
    week_filter = week_chosen

filtered = streamlit_data[(streamlit_data['BRAND_NAME'].isin(brand_filter) & (streamlit_data['HOTEL_COUNTRY_NAME'].isin(country_filter)) 
                            # & (streamlit_data['Hotel_State_Name'].isin(state_filter))
                            & (streamlit_data['METRO_REGION_NAME'].isin(metro_filter))
                            & (streamlit_data['WEEK_BEGIN_DATE'].isin(week_filter)) 
                            & (streamlit_data['METRO_REGION_NAME'].isin(top_20_metros)))
                            & (streamlit_data['WEEK_BEGIN_DATE'] >= date_begin_chosen) 
                            & (streamlit_data['WEEK_BEGIN_DATE'] <= date_end_chosen)]

# st.dataframe(filtered)

st.write('Aggregation:')

chosen_metric = st.selectbox('Performance Metric:', ['RMNTS_CY','ORDERS','ADR'])

if chosen_metric == 'RMNTS_CY':
    chosen_aggregation = st.selectbox('Aggregation Type:', ['sum','mean','median','max','min'])
elif chosen_metric == 'ORDERS':
    chosen_aggregation = st.selectbox('Aggregation Type:', ['sum','mean','median','max','min'])
elif chosen_metric == 'ADR':
    chosen_aggregation = st.selectbox('Aggregation Type:', ['mean','median','max','min'])

if chosen_metric == 'RMNTS_CY':
    chosen_metric_py = 'RMNTS_PY'
elif chosen_metric == 'ORDERS':
    chosen_metric_py = 'ORDERS_PY'
elif chosen_metric == 'ADR':
    chosen_metric_py = 'ADR_PY'

# if chosen_metric == 'RMNTS_CY':


# filtered['RMNTS_YOY'] = (filtered['RMNTS_CY'] - filtered['RMNTS_PY']) / filtered['RMNTS_PY']
# filtered['RMNTS_YOY'] = filtered['RMNTS_YOY'].astype(str) + '%'

# st.write(filteref)

dataframe = filtered
selected_attribute = attribute_selection

def analysis():
    agg_func_math = {
    chosen_metric:
    chosen_aggregation,chosen_metric_py:chosen_aggregation
    }
    if attribute_selection in ("", []):
        st.write("DATA NOT IN FILE")
    # elif chosen_metric == 'ADR':
    #     groupby = dataframe.groupby(selected_attribute,as_index=False).agg(agg_func_math)
    #     groupby['ADR_YOY'] = (100 * (groupby['ADR'] - groupby['ADR_PY']) / groupby['ADR_PY']).astype(float).round(3)
    #     groupby['ADR_YOY'] = groupby['ADR_YOY'].astype(str) + '%'
    #     # dataframe['RMNTS_WoW'] = (dataframe['RMNTS_CY'] - dataframe['RMNTS_PW']) / dataframe['RMNTS_PW']
        # st.dataframe(groupby)
    elif chosen_metric == 'RMNTS_CY':
        groupby = dataframe.groupby(selected_attribute,as_index=False).agg(agg_func_math)
        groupby['RMNTS_YOY'] = (100 * (groupby['RMNTS_CY'] - groupby['RMNTS_PY']) / groupby['RMNTS_PY']).astype(float).round(3)
        groupby['RMNTS_YOY'] = groupby['RMNTS_YOY'].astype(str) + '%'
        # dataframe['RMNTS_WoW'] = (dataframe['RMNTS_CY'] - dataframe['RMNTS_PW']) / dataframe['RMNTS_PW']
        st.dataframe(groupby)
    else: 
        st.write("No attributes selected")

analysis()

st.write('Share:')

def percent_out_of_total(attribute):
    if attribute in ("",[]):
        st.write("No attributes selected")
        # rmnts_gb = filtered.groupby(attribute,as_index=False)['RMNTS_CY'].sum()
        # st.write(rmnts_gb) 
    else:
        chosen_total = filtered.groupby(attribute,as_index=False)['RMNTS_CY'].sum()
        chosen_total['Total'] = chosen_total['RMNTS_CY'].sum().astype(float).round(1)
        chosen_total['Percent_Out_Of_Total'] = (100 * ((chosen_total['RMNTS_CY'] / chosen_total['Total']))).astype(float).round(3)
        chosen_total['Percent_Out_Of_Total'] = chosen_total['Percent_Out_Of_Total'].astype(str) + '%'
        chosen_total.reset_index(drop=True)
        sorted_total = chosen_total.sort_values(by='RMNTS_CY', ascending=False)
        st.write(sorted_total)

percent_out_of_total(attribute_selection)




if attribute_selection in ("",[]):
        st.write("No attributes selected")
else:   
    # dataframe = filtered
    # filter_by = attribute_selection

    # created_list = dataframe[filter_by].unique().tolist()
    # filtered_dict = {}

    # for kind in created_list:
    #     filtered_dict[kind] = dataframe[dataframe[filter_by] == kind]

    # def analysis():
    #     for key, value in filtered_dict.items():
    #         rmnts = filtered_dict[key][['RMNTS_CY','RMNTS_PY']].corr()

    #         st.write("",key,rmnts)

    # analysis()

    if brand_owner_chosen in ("",[]):

        xaxis = 'WEEK_BEGIN_DATE'
        newdataframe = dataframe.groupby(['WEEK_BEGIN_DATE'],as_index=False).agg({'RMNTS_CY':'sum','RMNTS_PY':'sum'})

        def analysis():
                fig = make_subplots(rows=1, cols=2, shared_xaxes=True, shared_yaxes=False, specs=[[{}, {}]])

                fig.add_trace(
                go.Scatter(x=newdataframe[xaxis], y=newdataframe['RMNTS_CY'], name="RMNTS"),
                secondary_y=False, 
                )

                fig.add_trace(
                    go.Scatter(x=newdataframe[xaxis], y=newdataframe['RMNTS_PY'], name="RMNTS_PY"),
                    secondary_y=False,
                )

                fig.update_xaxes(title_text="WEEK_BEGIN_DATE",
                # tickformat="%q\n%Y",
                fixedrange=True,matches=None)
                fig.update_layout(title='All Brands',width=900,height=400)
                fig.update_yaxes(rangemode="tozero")

                st.plotly_chart(fig, use_container_width=True)


        analysis()
    
    elif brand_owner_chosen not in ("",[]):
                # st.write(dataframe)
        filter_by = attribute_selection

        xaxis = 'WEEK_BEGIN_DATE'
        newdataframe = dataframe.groupby(['WEEK_BEGIN_DATE','BRAND_NAME'],as_index=False).agg({'RMNTS_CY':'sum','RMNTS_PY':'sum'})

        created_list = brand_owner_chosen
        filtered_dict = {}

        for kind in created_list:
            filtered_dict[kind] = newdataframe[newdataframe[filter_by] == kind]

        def analysis2():
            for key, value in filtered_dict.items():
                fig = make_subplots(specs=[[{"secondary_y": True}]],)


                fig.add_trace(
                go.Scatter(x=filtered_dict[key][xaxis], y=filtered_dict[key]['RMNTS_CY'], name="RMNTS"),
                secondary_y=False, 
                )

                fig.add_trace(
                    go.Scatter(x=filtered_dict[key][xaxis], y=filtered_dict[key]['RMNTS_PY'], name="RMNTS_PY"),
                    secondary_y=False,
                )

                fig.update_xaxes(title_text="WEEK_BEGIN_DATE",
                # tickformat="%q\n%Y",
                fixedrange=True,matches=None)
                fig.update_layout(title=key,width=900,height=400)
                fig.update_yaxes(rangemode="tozero")

                st.plotly_chart(fig, use_container_width=True)


        analysis2()


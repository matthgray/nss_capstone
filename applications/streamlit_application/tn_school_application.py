# needed packages
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

# read data
# url
#url='https://raw.githubusercontent.com/matthgray/nss_capstone/mg_eda/data/clean_data/clean_data.csv'
tn_data = pd.read_csv('streamlit_application_data_3.csv')
finance_data = pd.read_csv('finance_county_1.csv')


# how to filter by columns?
# matp
fig_zip = px.scatter_mapbox(finance_data, lat="latitude", lon="longitude",color='Total_Expenditures_Per_School', size="State_Percentage",
                  color_continuous_scale=px.colors.cyclical.Edge, size_max=15, zoom=5,hover_name="district_name",
                  mapbox_style="carto-positron")
fig_zip


# filter by county
sorted_county = sorted(tn_data.district_name.unique())
selected_from_county =st.sidebar.multiselect('filter by county',sorted_county,default='Metro Nashville Public Schools')
county_selected = tn_data[(tn_data.district_name.isin(selected_from_county))]

# select a metric
unique_metric = sorted(tn_data.columns.unique())
selected_metric = st.sidebar.multiselect('choose a metric', unique_metric,default=['score_achievement'])
#filter_metric=county_selected[(county_selected[selected_metric]) & (county_selected[['school_name']])]


#st.line_chart(filter_metric)

#unique_pos = ['RB','QB','WR','FB','TE']
#fig = px.bar(filter_metric, x=selected_metric, y='school_name')
#fig


# Filtering data
#df_selected = tn_data[(county_selected) & (filter_metric)]


#figed = px.treemap(county_selected, path=['school_name'], values='dropout_rate',hover_data=['district_name','graduation rate '])
#figed


st.dataframe(county_selected)

#st.write(county_selected.percent_scoring_21_or_higher.describe(),county_selected.percent_scoring_below_19.describe())

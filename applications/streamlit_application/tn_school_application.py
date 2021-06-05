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
finance_data = pd.read_csv('tn_map_data.csv')
tn_data = tn_data.dropna()


#----------------------------------------------------------------#
# Titles

st.markdown('''# TN SCHOOLS''')
st.markdown("""**DATA SOURCE:** [TN.gov](https://www.tn.gov/education/data/data-downloads.html) """)
st.markdown("""**DEFINITIONS:**[TN.GOV/DEFINITIONS](https://www.tn.gov/content/dam/tn/education/data/data_definitions.pdf)""")
st.write('''# Score achievement and per pupil spending in 2019 by county''')

#------------------------------------------------------------#
# filters
# filter by county
sorted_county = sorted(tn_data.district_name.unique())
selected_from_county =st.sidebar.multiselect('filter by county',sorted_county,default='Metro Nashville Public Schools')
#county_selected = tn_data[(tn_data.district_name.isin(selected_from_county))]

#select high school or k8
sort_school = sorted(tn_data.pool.unique())
selected_from_school= st.sidebar.multiselect('filter by school',sort_school,default='K8')
#select_df=county_selected[(county_selected)&(tn_data[(tn_data.district_name.isin(selected_from_county)))]



df_selected_school = tn_data[(tn_data.district_name.isin(selected_from_county)) & (tn_data.pool.isin(selected_from_school))]

#------------------------------------------------------------------#
# graphs

fig_zip = px.scatter_mapbox(finance_data, lat="latitude", lon="longitude",color='score_achievement', size="district_ppe",
                  color_continuous_scale=px.colors.cyclical.Edge, size_max=15, zoom=5,hover_name="district_name",
                  mapbox_style="carto-positron")
fig_zip

st.write('''# Score achievement and local spending by county  ''')
fig_zip_score = px.scatter_mapbox(finance_data, lat="latitude", lon="longitude",color='score_achievement', size="local_funding_percent",
                  color_continuous_scale=px.colors.cyclical.Edge, size_max=15, zoom=5,hover_name="district_name",
                  mapbox_style="carto-positron")
fig_zip_score

st.dataframe(df_selected_school)

st.write('''# Schools with the highest achievement score from 2019 by county:''')
figed = px.treemap(df_selected_school, path=['district_name','school_name'], values='score_achievement', color='district_name',hover_data=['zipcode','district_name'])
figed


st.write('''# Schools with highest percentage of students absent & teachers retained: ''')
teacher_retention=df_selected_school['percent_retained'].mean()
figed = px.treemap(df_selected_school, path=['district_name','zipcode','school_name'] , values='percent_ca2019',color='school_name',hover_data=['zipcode','district_name'])
figed

fig_teacher = px.histogram(df_selected_school.sort_values('percent_ca2019'), x="percent_ca2019",y='school_name', color="district_name")
fig_teacher

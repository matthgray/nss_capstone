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
tn_data = pd.read_csv('clean_data.csv')

# matp
st.map(tn_data)
# filter by county
sorted_county = sorted(tn_data.district_name.unique())
selected_from_county =st.sidebar.multiselect('filter by county',sorted_county)
county_selected = tn_data[(tn_data.district_name.isin(selected_from_county))]

# select columns
sorted_metric = sorted(tn_data.columns.unique())
selected_from_metric = st.sidebar.multiselect('choose a metric', sorted_metric)




st.dataframe(county_selected)

st.write(county_selected.percent_scoring_21_or_higher.describe(),county_selected.percent_scoring_below_19.describe())

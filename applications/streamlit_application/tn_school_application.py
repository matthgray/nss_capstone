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
# https://raw.githubusercontent.com/matthgray/nss_capstone/mg_eda/data/clean_data/clean_data.csv
hop_data = pd.read_csv('hops_final_clean.csv')

# filter by county
sorted_fnpi = sorted(hop_data.from_npi.unique())
selected_from_npi =st.sidebar.multiselect('filter by from npi',sorted_fnpi,default=1093741464)
npi_selected = hop_data[(hop_data.from_npi.isin(selected_from_npi))]

#filter by school

#filter by category that is suspension, dropout, etc..

st.dataframe(npi_selected)
st.write(npi_selected.patient_count.describe(),npi_selected.transaction_count.describe())

fig = px.treemap(hop_data, path=['from_npi'], values='patient_count')
fig
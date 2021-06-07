# needed packages
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

# read data
finance_url ='https://raw.githubusercontent.com/matthgray/nss_capstone/omega/data/tn_finance_data.csv'
achievement_url='https://raw.githubusercontent.com/matthgray/nss_capstone/omega/data/tn_grade_data.csv'
# data for achievement scores, teacher Retention,etc
finance_data = pd.read_csv(finance_url)
# data for ppe and budgets
tn_data = pd.read_csv(achievement_url)
tn_data = tn_data.dropna()
# fix henderson latitude & longitude
#finance_data['longitude']= finance_data['longitude'].replace('-88.4053','-86.6200')
#finance_data['latitude']= finance_data['latitude'].replace('35.6584','36.3048')

#----------------------------------------------------------------#
# Titles

st.markdown('''# TN SCHOOLS''')
st.markdown("""**DATA SOURCE:** [TN.gov](https://www.tn.gov/education/data/data-downloads.html) """)
st.markdown("""**DEFINITIONS:**[TN.GOV/DEFINITIONS](https://www.tn.gov/content/dam/tn/education/data/data_definitions.pdf)""")
#st.dataframe(finance_data)
#st.dataframe(tn_data)
#st.info(tn_data.dtypes)
#------------------------------------------------------------#

#sorted_finance=sorted(finance_data.district_name.unique())
#sected_from_finance= st.sidebar.multiselect('filter for map',sorted_finance,'Henderson County Schools')
#sort_finance_df=finance_data[(finance_data.district_name.isin(sected_from_finance))]

# filters
# filter by county
sorted_county = sorted(tn_data.district_name.unique())
selected_from_county =st.sidebar.multiselect('filter by county',sorted_county,
default=['Metro Nashville Public Schools','Trousdale County Schools','Murfreesboro City Schools','Wilson County School District','Henderson County Schools','Williamson County Schools'])
#county_selected = tn_data[(tn_data.district_name.isin(selected_from_county))]

#select high school or k8
sort_grade = sorted(tn_data.pool.unique())
selected_from_grade= st.sidebar.multiselect('filter by grade',sort_grade,'K8')



#select_df=county_selected[(county_selected)&(tn_data[(tn_data.district_name.isin(selected_from_county)))]

sort_school = sorted(tn_data.school_name.unique())
selected_from_school= st.sidebar.multiselect('filter by school',sort_school,
default=['Granbery Elementary','Trousdale Co Elementary','Westover Elementary','Bethesda Elementary','John Pittard Elementary','Watertown Elementary'])
#select_df=county_selected[(county_selected)&(tn_data[(tn_data.district_name.isin(selected_from_county)))]


school_selected_df= tn_data[(tn_data.school_name.isin(selected_from_school))]
df_selected_school = tn_data[(tn_data.district_name.isin(selected_from_county)) & (tn_data.pool.isin(selected_from_grade))]


# handle counties with not HS or K8
#if df_selected_school.pool = NaN:
    #st.success("Success!")
#else:
    #st.error('A county does not have a high school or K8 school. Please try removing one and see if that works.')

#------------------------------------------------------------------#
# graphs
#fig_a = px.sunburst(finance_data, path=['district_name'], values='local_funding_percent',
                 # color='district_name', hover_data=["score_achievement"],
                  #color_continuous_scale='RdBu')

#fig_a

st.write('''# Score achievement and local spending by county:  ''')
local_fig = px.scatter_mapbox(finance_data, lat="latitude", lon="longitude",color='score_achievement', size="local_funding_percent",title="Percentage of PPE that is locally funded and colored by achievement score",
                  hover_data=["district_ppe","state_funding_percent"], size_max=15, zoom=5,hover_name="district_name",
                  mapbox_style="carto-positron")
local_fig



st.write('''# Schools with the highest achievement score from 2019 by county:''')
achieve_fig = px.treemap(df_selected_school, path=['district_name','pool','school_name'], values='score_achievement', color='district_name',hover_data=['zipcode','district_name'],title="Achievement score by county")
achieve_fig

#fig = px.sunburst(df_selected_school, path=['district_name', 'school_name'], values='percent_retained',
                  #color='district_name', hover_data=["score_achievement","zipcode"],
                  #color_continuous_scale='RdBu')

#fig

st.write('''# Number of School Teachers and Teacher Retention by Schools: ''')
fig_absent = px.histogram(df_selected_school.sort_values('percent_retained'), x="percent_retained",y='school_name', color="district_name",title="The schools teacher retention",
hover_data=["score_achievement","zipcode"],
labels={'school_name':'SCHOOLS','percent_ca2019':'PERCENTAGE OF STUDENTS ABSENT'})

fig_absent

st.write('''# Schools with highest percentage of students absent: ''')
teacher_fig = px.bar(school_selected_df.sort_values('enrollment_2019'), x='enrollment_2019', y='school_name',
              color='percent_ca2019',hover_data=['enrollment_2019','score_achievement','percent_ca2019','district_name','teacher'],title="Chronically Absent per school",
              labels={'school_name':'SCHOOLS','enrollment_2019':'STUDENT ENROLLMENT','percent_ca2019':'PERCENTAGE OF STUDENT CHRONICALLY ABSENT'},
              height=400)
teacher_fig

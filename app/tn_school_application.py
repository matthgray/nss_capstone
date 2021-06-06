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


#----------------------------------------------------------------#
# Titles

st.markdown('''# TN SCHOOLS''')
st.markdown("""**DATA SOURCE:** [TN.gov](https://www.tn.gov/education/data/data-downloads.html) """)
st.markdown("""**DEFINITIONS:**[TN.GOV/DEFINITIONS](https://www.tn.gov/content/dam/tn/education/data/data_definitions.pdf)""")

#st.dataframe(tn_data)
#st.info(tn_data.dtypes)
#------------------------------------------------------------#
# filters
# filter by county
sorted_county = sorted(tn_data.district_name.unique())
selected_from_county =st.sidebar.multiselect('filter by county',sorted_county,default=['Metro Nashville Public Schools','Trousdale County Schools','Maryville City Schools'])
#county_selected = tn_data[(tn_data.district_name.isin(selected_from_county))]

#select high school or k8
sort_grade = sorted(tn_data.pool.unique())
selected_from_grade= st.sidebar.multiselect('filter by grade',sort_grade,sort_grade)



#select_df=county_selected[(county_selected)&(tn_data[(tn_data.district_name.isin(selected_from_county)))]

sort_school = sorted(tn_data.school_name.unique())
selected_from_school= st.sidebar.multiselect('filter by school',sort_school,
default=['Granbery Elementary','John Sevier Elementary','Trousdale Co Elementary'])
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


st.write('''# Score achievement and local spending by county:  ''')
local_fig = px.scatter_mapbox(finance_data, lat="latitude", lon="longitude",color='score_achievement', size="local_funding_percent",title="Percentage of PPE that is locally funded and colored by achievement score",
                  hover_data=["district_ppe","state_funding_percent"],color_continuous_scale=px.colors.cyclical.Edge, size_max=15, zoom=5,hover_name="district_name",
                  mapbox_style="carto-positron")
local_fig



st.write('''# Schools with the highest achievement score from 2019 by county:''')
achieve_fig = px.treemap(df_selected_school, path=['district_name','pool','school_name'], values='score_achievement', color='district_name',hover_data=['zipcode','district_name'],title="Achievement score by county")
achieve_fig


st.write('''# Schools with highest percentage of students absent: ''')


fig_absent = px.histogram(df_selected_school.sort_values('percent_ca2019'), x="percent_ca2019",y='school_name', color="district_name",title="Chronically Absent per school",
hover_data=["score_achievement","zipcode"],
labels={'school_name':'SCHOOLS','percent_ca2019':'PERCENTAGE OF STUDENTS ABSENT'})

fig_absent

st.write('''# Number of School Teachers and Teacher Retention by Schools: ''')
teacher_fig = px.bar(school_selected_df.sort_values('teacher'), x='teacher', y='school_name',title="Number of teachers per school and the schools teacher retention",
              color='percent_retained',hover_data=['enrollment_2019','score_achievement','percent_ca2019','district_name'],
              labels={'school_name':'SCHOOLS','pct_chronically_absent_2020':'PERCENTAGE OF STUDENTS ABSENT','percent_retained':'PERCENTAGE OF TEACHERS RETAINED'},
              height=400)
teacher_fig

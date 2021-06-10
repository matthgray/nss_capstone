

# needed packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import time
# read data
finance_url ='https://raw.githubusercontent.com/matthgray/nss_capstone/omega/data/clean_data/tn_finance_data.csv'
achievement_url='https://raw.githubusercontent.com/matthgray/nss_capstone/omega/data/clean_data/tn_grade_data.csv'
# data for achievement scores, teacher Retention,etc
finance_data = pd.read_csv(finance_url)
finance_data['score_achievement']=finance_data['score_achievement'].round(decimals=2)
# data for ppe and budgets
tn_data = pd.read_csv(achievement_url)
# creat a student to teacher ratio column
tn_data['student_teacher_ratio']=tn_data['students_enrolled'] / tn_data['number_of_teachers']
tn_data['student_teacher_ratio']=tn_data['student_teacher_ratio'].round(decimals=0)
#tn_data = tn_data.dropna()
# fix henderson latitude & longitude
#finance_data['longitude']= finance_data['longitude'].replace('-88.4053','-86.6200')
#finance_data['latitude']= finance_data['latitude'].replace('35.6584','36.3048')

#----------------------------------------------------------------#
# Titles
#st.dataframe(tn_data)
st.markdown('''# TN SCHOOLS ANALYSIS FOR 2019''')
st.markdown("""**DATA SOURCE:** [TN.gov](https://www.tn.gov/education/data/data-downloads.html) """)
st.markdown("""**DEFINITIONS:**[TN.GOV/DEFINITIONS](https://www.tn.gov/content/dam/tn/education/data/data_definitions.pdf)""")
#st.dataframe(finance_data)
#st.dataframe(tn_data)
#st.info(tn_data.dtypes)
#------------------------------------------------------------#
# filters
#sorted_finance=sorted(finance_data.district_name.unique())
#sected_from_finance= st.sidebar.multiselect('filter for map',sorted_finance,'Henderson County Schools')
#sort_finance_df=finance_data[(finance_data.district_name.isin(sected_from_finance))]

# filters
# filter by county
sorted_county = sorted(tn_data.district_name.unique())
selected_from_county =st.sidebar.multiselect('filter by county',sorted_county,
default=['Metro Nashville Public Schools','Achievement School District','Rutherford County Schools','Williamson County Schools','Wilson County School District','Sumner County Schools','Trousdale County Schools'])
#county_selected = tn_data[(tn_data.district_name.isin(selected_from_county))]

#select high school or k8
sort_grade = sorted(tn_data.pool.unique())
selected_from_grade= st.sidebar.multiselect('filter by grade',sort_grade,'K8')



#select_df=county_selected[(county_selected)&(tn_data[(tn_data.district_name.isin(selected_from_county)))]

sort_school = sorted(tn_data.school_name.unique())
selected_from_school= st.sidebar.multiselect('filter by school',sort_school,
default=['Trousdale Co Elementary','Harpeth Valley Elementary','Springdale Elementary School',
'Lipscomb Elementary','Lakeside Park Elementary','McFadden School Of Excellence','Corning Achievement Elementary'])
#'Oak View Elem School','Rucker Stewart Middle','Whitworth-Buchanan Middle School','Watertown Middle School','Stratton Elementary
#default=['Granbery Elementary','Trousdale Co Elementary','Westover Elementary','Bethesda Elementary','John Pittard Elementary','Watertown Elementary'])
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


st.write('''# Score achievement is the color and local spending is the size of the circle:''')
local_fig = px.scatter_mapbox(finance_data, lat="latitude", lon="longitude",color='score_achievement',
                  size="local_funding_percent",
                  title="The size of the circle is the percentage of per pupil expenditure that is locally funded and the color is the achievement score",
                  hover_data=["district_ppe"], size_max=15, zoom=5,hover_name="district_name",
                  mapbox_style="carto-positron", color_continuous_scale='spectral',labels={'score_achievement':'Average Score Achievement by District'})

local_fig




st.write('''# Schools with the highest achievement score from 2019 by county:''')
#achieve_fig = px.histogram(df_selected_school.sort_values('score_achievement'), x="score_achievement",y='school_name',
#                    color="district_name",title="Colors are the districts,x axis is the achievement score of the class, and y axis are the schools in the district",
#                    hover_data=['zipcode','district_name','score_achievement'],
#labels={'school_name':'SCHOOLS','score_achievement':'Score achievement  by District','district_name':'District'})
#achieve_fig

fig = px.treemap(df_selected_school.sort_values('score_achievement'),path =('district_name','pool','school_name'),values = 'score_achievement',
color = 'district_name',hover_data=['zipcode','district_name','score_achievement','percent_retained'],title="The color shows the district, the size of square is the schools achvievment scores",
                   labels={'score_achievement':'Achievement Score','district_name':'District','score_achievement':'Achievement Score'},hover_name="school_name")
fig


st.write('''# Achievement score by teacher retention with size of the circle as number of teachers at the school: ''')

teacher_fig=px.scatter(school_selected_df.sort_values('school_name'), x="percent_retained",y='score_achievement',size='student_teacher_ratio',
                    title="Achievement score by teacher retention with size of the circle as number of teachers at the school",
                    labels={'percent_retained':'Percentage of teacher retention','score_achievement':'Achievement Score','school_name':'School'},
                    color="school_name",hover_data=['percent_ca','percent_retained','district_name'],hover_name="district_name")

teacher_fig


st.write('''# Achievement score by chronically absent students with size of the circle as student enrollment: ''')
#student_fig = px.bar(school_selected_df.sort_values('students_enrolled'), x='students_enrolled', y='school_name',
#              color='percent_ca',hover_data=['students_enrolled','score_achievement','percent_ca','district_name','number_of_teachers','percent_retained'],title="Chronically Absent per school",
#              labels={'school_name':'SCHOOLS','students_enrolled':'STUDENT ENROLLMENT','percent_ca':'PERCENTAGE OF STUDENT CHRONICALLY ABSENT'}, color_continuous_scale='rdylgn')
             # height=400)
#student_fig
#school_selected_df.sort_values('percent_ca')
student_fig = px.scatter(school_selected_df.sort_values('school_name'), x="percent_ca", y="score_achievement",
	         size="students_enrolled", color="school_name",title="Achievement score by chronically absent students with size of the circle as student enrollment",
             labels={'school_name':'School','percent_retained':'Percentage of teacher retention','score_achievement':'Achievement Score','students_enrolled':'STUDENT ENROLLMENT','percent_ca':'PERCENTAGE OF STUDENT CHRONICALLY ABSENT'},
                 hover_name="district_name", log_x=True, size_max=60)
student_fig
#st.info(df_selected_school.shape)
#------------------------------------------#
# recap
#st.dataframe(df_selected_school)
if st.button("RECAP"):
    st.write("# TROUSDALE, SUMNER, WILSON, WILLIAMSON,and RUTHERFORD ARE COMPETING WITH NASHVILLE")
    st.write("# TROUSDALE IS SPENDING THE LOWEST AND ACHIEVING THE MOST IN MIDDLE TN")
# final
if st.button("WHICH COUNTY HAS THE BEST SCHOOLS?"):
    with st.spinner('Wait for it...'):
        time.sleep(1)
    st.balloons()
    st.success("CONGRATS!")
    st.write("# WILLIAMSON COUNTY IS OUR WINNER!")

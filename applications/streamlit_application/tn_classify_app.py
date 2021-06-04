import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve,auc
from sklearn.metrics import RocCurveDisplay
from sklearn.feature_selection import mutual_info_regression
from sklearn import metrics
import matplotlib.pyplot as plt

df=pd.read_csv('school_classification_data.csv')

st.set_page_config(page_title='The Machine Learning for TN Education',
    layout='wide')

st.write('# Predicting Dropout out schools')

def build_model(df):
    X = df.iloc[:,:-1] # Using all column except for the last column as X
    Y = df.iloc[:,-1] # Selecting the last column as Y


    # Data splitting
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=(100-split_size)/100)


    st.markdown('**1.2. Data splits**')
    st.write('Training set')
    st.info(X_train.shape)
    st.write('Test set')
    st.info(X_test.shape)

    st.markdown('**1.3. Variable details**:')
    st.write('X variable')
    st.info(list(X.columns))
    st.write('Y variable')
    st.info(Y.name)

    rf = RandomForestClassifier(n_estimators=parameter_n_estimators,
        random_state=parameter_random_state,
        max_features=parameter_max_features,
        criterion=parameter_criterion,
        min_samples_split=parameter_min_samples_split,
        min_samples_leaf=parameter_min_samples_leaf,
        bootstrap=parameter_bootstrap,
        oob_score=parameter_oob_score,
        n_jobs=parameter_n_jobs)
    rf.fit(X_train, Y_train)

    st.subheader('2. Model Performance')

    st.markdown('**2.1. Training set**')
    Y_pred_train = rf.predict(X_train)
    st.write('Area Under the Curve:')
    st.info( metrics.roc_auc_score(Y_train, Y_pred_train) )

    fpr, tpr, thresholds = roc_curve(Y_train, Y_pred_train)
    fig1 = px.area(
    x=fpr, y=tpr,
    title=f'ROC Curve (AUC={auc(fpr, tpr):.4f})',
    labels=dict(x='False Positive Rate', y='True Positive Rate'),
    width=700, height=500
    )
    fig1.add_shape(
    type='line', line=dict(dash='dash'),
    x0=0, x1=1, y0=0, y1=1
    )

    fig1.update_yaxes(scaleanchor="x", scaleratio=1)
    fig1.update_xaxes(constrain='domain')
    fig1

    #st.write('Error (MSE or MAE):')
    #st.info( mean_squared_error(Y_train, Y_pred_train) )

    st.markdown('**2.2. Test set**')
    Y_pred_test = rf.predict(X_test)
    st.write('Area Under the Curve:')
    st.info(metrics.roc_auc_score(Y_test, Y_pred_test))


    fpr, tpr, thresholds = roc_curve(Y_test, Y_pred_test)
    fig = px.area(
    x=fpr, y=tpr,
    title=f'ROC Curve (AUC={auc(fpr, tpr):.4f})',
    labels=dict(x='False Positive Rate', y='True Positive Rate'),
    width=700, height=500
    )
    fig.add_shape(
    type='line', line=dict(dash='dash'),
    x0=0, x1=1, y0=0, y1=1
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_xaxes(constrain='domain')
    fig

    #st.info( metrics.roc_curve(Y_test, Y_pred_test) )

    #st.write('Error (MSE or MAE):')
    #st.info( mean_squared_error(Y_test, Y_pred_test) )

    st.subheader('3. Model Parameters')
    st.write(rf.get_params())
#--------------------------------------------------------------#
# Sidebar - Specify parameter settings
with st.sidebar.header('2. Set Parameters'):
    split_size = st.sidebar.slider('Data split ratio (% for Training Set)', 10, 90, 80, 5)

with st.sidebar.subheader('2.1. Learning Parameters'):
    parameter_n_estimators = st.sidebar.slider('Number of estimators (n_estimators)', 0, 1000, 100,10)
    parameter_max_features = st.sidebar.select_slider('Max features (max_features)', options=['auto'])
    parameter_min_samples_split = st.sidebar.slider('Minimum number of samples required to split an internal node (min_samples_split)', 1, 10, 2, 1)
    parameter_min_samples_leaf = st.sidebar.slider('Minimum number of samples required to be at a leaf node (min_samples_leaf)', 1, 10, 2, 1)

with st.sidebar.subheader('2.2. General Parameters'):
    parameter_random_state = st.sidebar.slider('Seed number (random_state)', 0, 1000, 42, 1)
    parameter_criterion = st.sidebar.select_slider('Performance measure (criterion)', options=['gini', 'entropy'])
    parameter_bootstrap = st.sidebar.select_slider('Bootstrap samples when building trees (bootstrap)', options=[True, False])
    parameter_oob_score = st.sidebar.select_slider('Whether to use out-of-bag samples to estimate the generalization score. Only available if bootstrap=True.', options=[False, True])
    parameter_n_jobs = st.sidebar.select_slider('Number of jobs to run in parallel (n_jobs)', options=[1, -1])

#----------------------------------------------------------------------------------------------------------#
st.subheader('1. Dataset')

if st.button('Press to build a classification model'):
build_model(df)

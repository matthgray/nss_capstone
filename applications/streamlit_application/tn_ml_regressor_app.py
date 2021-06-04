import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
import shap
import plotly.express as px
from matplotlib import pyplot as plt

#data
df=pd.read_csv('tn_reg_ml_data.csv')

st.write("# Predicting a schools graduation rate")
#---------------------------------#
# Model building
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

    rf = RandomForestRegressor(n_estimators=parameter_n_estimators,
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
    st.write('Coefficient of determination ($R^2$):')
    st.info( r2_score(Y_train, Y_pred_train) )

    st.write('Error (MSE or MAE):')
    st.info( mean_squared_error(Y_train, Y_pred_train) )

    st.markdown('**2.2. Test set**')
    Y_pred_test = rf.predict(X_test)
    st.write('Coefficient of determination ($R^2$):')
    st.info( r2_score(Y_test, Y_pred_test) )

    st.write('Error (MSE or MAE):')
    st.info( mean_squared_error(Y_test, Y_pred_test) )

    st.subheader('3. Model Parameters')
    st.write(rf.get_params())
    st.subheader('4. Important features')
    sorted_idx = rf.feature_importances_.argsort()
    fig=px.bar(df.columns[sorted_idx], rf.feature_importances_[sorted_idx])
    fig
    st.info(df.shape)
    st.dataframe(df)


#---------------------------------#

# Sidebar - Specify parameter settings
with st.sidebar.header('2. Set Parameters'):
    split_size = st.sidebar.slider('Data split ratio (% for Training Set)', 10, 90, 80, 5)

with st.sidebar.subheader('2.1. Learning Parameters'):
    parameter_n_estimators = st.sidebar.slider('Number of estimators (n_estimators)', 0, 1000, 100, 100)
    parameter_max_features = st.sidebar.select_slider('Max features (max_features)', options=['auto', 'sqrt', 'log2'])
    parameter_min_samples_split = st.sidebar.slider('Minimum number of samples required to split an internal node (min_samples_split)', 1, 10, 2, 1)
    parameter_min_samples_leaf = st.sidebar.slider('Minimum number of samples required to be at a leaf node (min_samples_leaf)', 1, 10, 2, 1)

with st.sidebar.subheader('2.2. General Parameters'):
    parameter_random_state = st.sidebar.slider('Seed number (random_state)', 0, 1000, 42, 1)
    parameter_criterion = st.sidebar.select_slider('Performance measure (criterion)', options=['mse', 'mae'])
    parameter_bootstrap = st.sidebar.select_slider('Bootstrap samples when building trees (bootstrap)', options=[True, False])
    parameter_oob_score = st.sidebar.select_slider('Whether to use out-of-bag samples to estimate the R^2 on unseen data (oob_score)', options=[False, True])
    parameter_n_jobs = st.sidebar.select_slider('Number of jobs to run in parallel (n_jobs)', options=[1, -1])

#---------------------------------#
if st.button('Press to build a model'):
    build_model(df)

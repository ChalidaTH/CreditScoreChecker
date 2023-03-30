# Import Libraries
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier
#from sklearn import model_selection
#from sklearn.preprocessing import MinMaxScaler 
from sklearn.ensemble import GradientBoostingClassifier

# Set Page configuration
# Read more at https://docs.streamlit.io/1.6.0/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title='Credit Score checker for housing loan', page_icon='🏘️', layout='wide', initial_sidebar_state='expanded')

# Set title of the app
st.title('🏘️ Credit Score self-checker for housing loan')

# Load data
df = pd.read_csv('loan_streamlit.csv')

# Set input widgets
st.sidebar.subheader('Input your credentials')
First = st.sidebar.slider('First time home owner', 0, 1, 1)
IncomePerBo = st.sidebar.slider('Income (USD)', 0, 500000, 2500)
UPB = st.sidebar.slider('Current amount of outstanding debt', 5000,1000000,50000)
Amount = st.sidebar.slider('Amount needed for housing loan', 10000, 1000000, 70000)
Front = st.sidebar.slider('Expexted housing payment to income (%)', 0, 100, 20)
Back = st.sidebar.slider('Total debt to your (%)', 0, 100, 30)

# Create feature matrix (X).
X = df[['IncomePerBo','UPB','First', 'Amount', 'Front', 'Back']]

# Create response vector (y).
y = df.BoCreditScore

# Define the model and fit the training data
gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gbc.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = gbc.predict(X_test)

# Use the trained model to make predictions on the training dataset
y_pred_train = gbc.predict(X_train)

# credit score table
Score_table = {'Credit Score Group': ['5', '4', '3', '2','1'],
        'Credit Score Category': ['Highest', 'High', 'Medium', 'Low', 'Lowest'],
        'FICO Credit Score Value': ['>=760', '700-159', '660-659', '621-659','<=620']}

# Display EDA
st.subheader('Exploratory Data Analysis')
st.write('The data is grouped by the credit score class and the variable mean is computed for each class.')
groupby_species_mean = df.groupby('BoCreditScore').mean()
st.write(groupby_species_mean)


# Create a Pandas dataframe from the data
score_df = pd.DataFrame(Score_table)

# Display the dataframe in a table using Streamlit
st.table(score_df)


# Print predicted flower species
st.subheader('Prediction')
st.metric('Predicted Credit Score class is :', y_pred[0], '')

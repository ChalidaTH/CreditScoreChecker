# Import Libraries
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier

# Set Page configuration
# Read more at https://docs.streamlit.io/1.6.0/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title='Credit Score self-checker for housing loan', page_icon='🏘️', layout='wide', initial_sidebar_state='expanded')

# Set title of the app
st.title('🏘️ Credit Score self-checker for housing loan')

# Load data
df = pd.read_csv('loan_streamlit.csv')

# Set input widgets
st.sidebar.subheader('Input your credentials')
First = st.sidebar.slider('1. Are you a first time home owner [No=0, Yes=1]?', 0, 1, 1)
IncomePerBo = st.sidebar.slider('2. Please select your yearly Income (USD)', 0, 500000, 2500)
UPB = st.sidebar.slider('3. Please state the current amount of your outstanding debt', 5000,1000000,50000)
Amount = st.sidebar.slider('4. Please state the amount needed for your housing loan', 10000, 1000000, 70000)
Front = st.sidebar.slider('5. Please state the expected mortgage principal, interest and housing payment to your income (%)', 0, 20, 100)
Back = st.sidebar.slider('6. Please state total debt including housing payment to your income (%)', 0, 30, 100)

# Separate to X and y
X = df.drop('BoCreditScore', axis=1)
y = df.BoCreditScore

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Build model
model = RandomForestClassifier(n_estimators=50, max_depth=10, min_samples_split=2, random_state=42)
model.fit(X_train, y_train)

# Generate prediction based on user selected attributes
y_pred = model.predict([[IncomePerBo, UPB, Amount, Front, Back, First]])

# Display EDA
st.subheader('Exploratory Data Analysis')
st.write('The data is grouped by the credit score class and the variable mean is computed for each class.')
groupby_species_mean = df.groupby('BoCreditScore').mean()
st.write(groupby_species_mean)
st.bar_chart(groupby_species_mean.T)

# credit score table
Score_table = {'Credit Score Group': ['5', '4', '3', '2','1'],
        'Credit Score Category': ['Highest', 'High', 'Medium', 'Low', 'Lowest'],
        'FICO Credit Score Value': ['>=760', '700-159', '660-659', '621-659','<=620']}

# Create a Pandas dataframe from the data
score_df = pd.DataFrame(Score_table)

# Display the dataframe in a table using Streamlit
st.table(score_df)


# Print predicted flower species
st.subheader('Prediction')
st.metric('Predicted Credit Score class is :', y_pred[0], '')

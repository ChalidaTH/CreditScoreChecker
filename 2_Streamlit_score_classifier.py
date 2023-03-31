# Import Libraries
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection
from sklearn.preprocessing import MinMaxScaler 
from PIL import Image
import pickle
from sklearn.ensemble import GradientBoostingClassifier

# Set Page configuration
# Read more at https://docs.streamlit.io/1.6.0/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title='Credit Score checker for housing loan', page_icon='🏘️', layout='wide', initial_sidebar_state='expanded')

# Set title of the app
st.title('Credit Score self-checker for housing loan')

image = Image.open('house.jpg')
st.image(image, caption='Mortgage Loan image from Realty Biz News ')

# Set input widgets
st.subheader('Input your credentials')

col1, col2, col3 = st.columns(3)

with col1:  
    IncomePerBo = st.slider('Income (USD)', 0, 500000, 1300)
    First = st.radio("First time home owner",('Yes', 'No'))
    if First == 'Yes':
        First = 1
    else:
        First = 0
    
with col2:
    UPB = st.slider('Current amount of outstanding debt', 5000,1000000,18000)
    Amount = st.slider('Amount needed for housing loan', 10000, 1000000, 180000)
    
with col3:
    Front = st.slider('Expexted housing payment to income (%)', 0, 100, 13)
    Back = st.slider('Total debt to your income (%)', 0, 100, 18)
    
submitted = st.button('Submit')
    
# load the model from disk
model = pickle.load(open('model.pkl', 'rb'))
    
# data frame of userinput
input_df = pd.DataFrame({'IncomePerBo':[IncomePerBo], 'UPB':[UPB], 'First': [First], 'Amount':[Amount], 'Front':[Front], 'Back':[Back] })
st.write(input_df)

#['IncomePerBo','UPB','First', 'Amount', 'Front', 'Back']
    
# Make predictions on the testing set
y_pred = model.predict(input_df)

# Print predicted flower species
st.subheader('Prediction')
if submitted:
    st.metric('Predicted', y_pred[0])

# credit score table
Score_table = {'Credit Score Group': ['5', '4', '3', '2','1'],
        'Credit Score Category': ['Highest', 'High', 'Medium', 'Low', 'Lowest'],
        'FICO Credit Score Value': ['>=760', '700-159', '660-659', '621-659','<=620']}

# Create a Pandas dataframe from the data
score_df = pd.DataFrame(Score_table)

# Display the dataframe in a table using Streamlit
st.table(score_df)

st.subheader('Average value in each class')
st.write('The data is grouped by the credit score class and the variable mean is computed for each class.')
groupby_species_mean = df.groupby('BoCreditScore').mean().applymap("{:,.0f}".format)

# Rename the columns
groupby_species_mean = groupby_species_mean.rename(columns={
    "BoCreditScore": "Borrowers' credit score",
    "IncomePerBo": "Income",
    "UPB": "Unpaid loan balance",
    "Amount": "Housing loan amount",
    "Front": "Housing payment to income ratio",
    "Back": "Debt payment to income ratio",
    "First": "First time home owner"
})

st.write(groupby_species_mean)

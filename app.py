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
    IncomePerBo = st.number_input('Insert annual Income (USD)')
    First = st.radio("First time home owner",('Yes', 'No'))
    if First == 'Yes':
        First = 1
    else:
        First = 0
    
with col2:
    UPB = st.number_input('Current amount of outstanding debt')
    Amount = st.number_input('Amount needed for housing loan')
    
with col3:
    Front = st.number_input('Expected housing payment to income (%)')
    Back = st.number_input('Total debt to your income (%)')
    
submitted = st.button('Submit')
    
# load the model from disk
model = pickle.load(open('model.pkl', 'rb'))
    
# data frame of userinput
input_df = pd.DataFrame({'IncomePerBo':[IncomePerBo], 'UPB':[UPB], 'First': [First], 'Amount':[Amount], 'Front':[Front], 'Back':[Back] })
st.write(input_df)

#['IncomePerBo','UPB','First', 'Amount', 'Front', 'Back']
    
# Make predictions on the testing set
y_pred = model.predict(input_df)

# Print predicted 
st.subheader('Prediction on your credit score')
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

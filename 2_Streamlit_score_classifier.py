# Import Libraries
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn.preprocessing import MinMaxScaler 

# Set Page configuration
# Read more at https://docs.streamlit.io/1.6.0/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title='Credit Score checker for housing loan', page_icon='🏘️', layout='wide', initial_sidebar_state='expanded')

# Set title of the app
st.title('🏘️ Credit Score self-checker for housing loan')

# Set input widgets
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Input your credentials')
    First = st.slider('First time home owner', 0, 1, 1)
    IncomePerBo = st.slider('Income (USD)', 0, 500000, 2500)

with col2:
    st.subheader(' ')
    UPB = st.slider('Current amount of outstanding debt', 5000,1000000,50000)
    Amount = st.slider('Amount needed for housing loan', 10000, 1000000, 70000)
    
with col3:
    st.subheader(' ')
    Front = st.slider('Expexted housing payment to income (%)', 0, 100, 20)
    Back = st.slider('Total debt to your income (%)', 0, 100, 30)

# Load data
df = pd.read_csv('loan_streamlit.csv')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[['IncomePerBo','UPB','Amount','Front','Back','First']],
                                                    df['BoCreditScore'], test_size=0.2, random_state=42)

# Normalize the data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the model using the best hyperparameters
model = RandomForestClassifier(n_estimators=50, max_depth=10, min_samples_split=2, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Print predicted flower species
st.subheader('Prediction')
st.metric('Predicted Credit Score class is :', y_pred[0], '')

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

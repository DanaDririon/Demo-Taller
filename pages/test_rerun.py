import streamlit as st
import pandas as pd

@st.cache(allow_output_mutation=True)
def create():
    d = {'id': ['a', 'b', 'c'], 'data': [3, 4,6]}
    df = pd.DataFrame(data=d)
    return df
df = create()
#create sidebar input
with st.sidebar.form("my_form"):
    a = st.slider('sidebar for testing', 5, 10, 9)
    calculate = st.form_submit_button('Calculate') 
 
if calculate:
    df['result'] = df['data'] + a 
    st.write(df)

filter = st.selectbox('filter data', df['id'].unique())
st.write(df[df['id'] == filter])
# Displaying the result consistently to be sure
st.table(df)
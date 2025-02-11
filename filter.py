import streamlit as st
import pandas as pd
import re

st.title("LP Service Provider Filter")

# Function to clean and transform Excel data into CSV-like format
def clean_excel_data(uploaded_file):
    cleaned_data_df = pd.read_excel(uploaded_file, sheet_name='Data', skiprows=5)
    
    cleaned_data_df.columns = cleaned_data_df.iloc[0]  
    cleaned_data_df = cleaned_data_df.drop(0)  
    
    # Drop columns that are unnecessary for analysis
    columns_to_drop = ['View Limited Partner Online']
    cleaned_data_df = cleaned_data_df.drop(columns=columns_to_drop, errors='ignore')
    
    cleaned_data_df = cleaned_data_df.reset_index(drop=True)
    return cleaned_data_df

# List of service providers to filter
fs_consultants = [
    "Mercer", "Cambridge Associates", "Wilshire Associates", "Aon Investments", 
    "Aon Hewitt", "Russell Investments", "Callan Investments", "NEPC", 
    "New England Pension Consultants", "Albourne Partners", "Callan Associates", "Aon"
]
pattern = re.compile("|".join(re.escape(provider) for provider in fs_consultants), re.IGNORECASE)

def uses_fs_consultant(services):
    if pd.isna(services):
        return 0
    return 1 if pattern.search(services) else 0

uploaded_file = st.file_uploader("Upload the LP file (Excel or CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    if uploaded_file.name.endswith("xlsx"):
        df = clean_excel_data(uploaded_file)  
    else:
        df = pd.read_csv(uploaded_file)  

    df['Uses FS Consultant'] = df['General Services'].apply(uses_fs_consultant)

    st.write("### Limited Partners with FS Consultant Status", df)

    if st.checkbox("Show only LPs without FS Consultants"):
        filtered_df = df[df['Uses FS Consultant'] == 0]
        st.write("### Limited Partners without FS Consultants", filtered_df)

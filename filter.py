import streamlit as st
import pandas as pd
import re

# Streamlit app title
st.title("LP Service Provider Filter")

# Function to clean and transform Excel data into CSV-like format
def clean_excel_data(uploaded_file):
    # Load the main sheet and skip metadata rows
    cleaned_data_df = pd.read_excel(uploaded_file, sheet_name='Data', skiprows=5)
    
    # Set proper headers and drop unnecessary columns
    cleaned_data_df.columns = cleaned_data_df.iloc[0]  # Set the headers from the first row
    cleaned_data_df = cleaned_data_df.drop(0)  # Drop the header row
    
    # Drop columns that are unnecessary for analysis
    columns_to_drop = ['View Limited Partner Online']
    cleaned_data_df = cleaned_data_df.drop(columns=columns_to_drop, errors='ignore')
    
    # Reset the index
    cleaned_data_df = cleaned_data_df.reset_index(drop=True)
    return cleaned_data_df

# List of service providers to filter
fs_consultants = [
    "Mercer", "Cambridge Associates", "Wilshire Associates", "Aon Investments", 
    "Aon Hewitt", "Russell Investments", "Callan Investments", "NEPC", 
    "New England Pension Consultants", "Albourne Partners", "Callan Associates", "Aon"
]

# Compile regex pattern to match any of the service providers (case-insensitive, handles whitespace)
pattern = re.compile("|".join(re.escape(provider) for provider in fs_consultants), re.IGNORECASE)

# Function to determine if any of the service providers are in the 'General Services'
def uses_fs_consultant(services):
    if pd.isna(services):
        return 0
    return 1 if pattern.search(services) else 0

# File uploader
uploaded_file = st.file_uploader("Upload the LP file (Excel or CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Check the file type and load data accordingly
    if uploaded_file.name.endswith("xlsx"):
        df = clean_excel_data(uploaded_file)  # Clean and load Excel data
    else:
        df = pd.read_csv(uploaded_file)  # Load CSV directly

    # Apply the function to create 'Uses FS Consultant' column
    df['Uses FS Consultant'] = df['General Services'].apply(uses_fs_consultant)

    # Display the entire dataframe with the new column
    st.write("### Limited Partners with FS Consultant Status", df)

    # Option to filter only rows where 'Uses FS Consultant' is 0
    if st.checkbox("Show only LPs without FS Consultants"):
        filtered_df = df[df['Uses FS Consultant'] == 0]
        st.write("### Limited Partners without FS Consultants", filtered_df)

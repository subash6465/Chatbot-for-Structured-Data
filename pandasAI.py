import streamlit as st
import pandas as pd
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
from pandasai import Agent
 
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def combing(files):
    
    # Read all CSV files into separate DataFrames
    data_frames = [pd.read_csv(file) for file in files]
 
    # Find common columns across all DataFrames
    common_cols = set(data_frames[0].columns)
    for df in data_frames[1:]:
        common_cols &= set(df.columns)
 
    # Merge DataFrames on common columns
    combined_df = data_frames[0]
    for df in data_frames[1:]:
        combined_df = pd.merge(combined_df, df, on=list(common_cols), how='inner')
 
    return combined_df
 
def chat_with_combined_csv(prompt, combined_df):
 
    # Initialize the OpenAI model
    llm = OpenAI(api_token=openai_api_key, model='gpt-3.5-turbo')
    agent = Agent(combined_df, config={"llm": llm})
 
    # Chat with the combined data
    result = agent.chat(prompt)
    return result
 
st.set_page_config(layout='wide')
st.title("Structured data processing")
 
# Upload multiple CSV files
input_csv_files = st.file_uploader("Upload your CSV files", type=['csv'], accept_multiple_files=True)
 
if input_csv_files:
    # Display the combined DataFrame
    combined_csv = combing(input_csv_files)
    st.subheader("Combined DataFrame")
    st.write(combined_csv) 
    # Display the combined DataFrame here
    # Chat with the combined data
    input_text = st.text_area("Enter your query for the combined data")
    if input_text:
        if st.button("Chat with Combined Data"):
            st.info(f"Your Query: {input_text}")
            result = chat_with_combined_csv(input_text, combined_csv)
            st.success(f"Combined Result: {result}")
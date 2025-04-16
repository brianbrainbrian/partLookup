import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Bin Lookup", layout="centered")

# Title
st.title("🔍 Bin Lookup")

# Load the Excel file
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("book1.xlsx")
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

df = load_data()

# Search bar
item_input = st.text_input("Enter Item Number:")

# Lookup logic
if item_input:
    result = df[df['Item No'].astype(str).str.strip() == item_input.strip()]

    if not result.empty:
        st.success("Item found!")
        st.write("**Bin Location:**", result.iloc[0]['binlocation'])
        st.write("**Description:**", result.iloc[0]['description'])
        st.write("**Quantity:**", result.iloc[0]['quantity'])
    else:
        st.warning("Item not found. Please check the Item Number.")

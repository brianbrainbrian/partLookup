import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Bin Lookup", layout="centered")

# Title
st.title("🔍 Bin Lookup")

# Load Excel file
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("book1.xlsx")
        df.columns = df.columns.str.strip()  # clean up column names
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

df = load_data()

# Search input
item_input = st.text_input("Enter Item Number:")

# Search result
# Search result
if item_input:
    result = df[df['Item No'].astype(str).str.strip().str.lower() == item_input.strip().lower()]
    
    if not result.empty:
        st.success("Item found!")
        st.write("**Bin Location Description:**", result.iloc[0]['Bin Location Description'])
        st.write("**Item Qty:**", result.iloc[0]['Item Qty'])
    else:
        st.warning("Item not found.")


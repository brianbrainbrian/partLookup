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
        df.columns = df.columns.str.strip()  # Clean column names
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

df = load_data()

# Check if required column exists
if "Item" not in df.columns:
    st.error("The Excel file must contain a column named 'Item'.")
    st.stop()

# Get list of unique items (sorted)
item_list = sorted(df['Item'].astype(str).str.strip().unique())

# User selection from dropdown
selected_item = st.selectbox("Select Item Number:", options=item_list)

# Show results
if selected_item:
    matches = df[df['Item'].astype(str).str.strip().str.lower() == selected_item.strip().lower()]
    
    if not matches.empty:
        st.success(f"Found {len(matches)} matching bin(s):")
        st.dataframe(matches[['Bin Location Description', 'Item Qty']].reset_index(drop=True))
    else:
        st.warning("Item not found.")

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
        df = pd.read_excel("apps/book1.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

df = load_data()

# Check for required columns
required_columns = ["Item", "Item Description", "Bin Location Description", "Item Qty"]
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    st.error(f"Missing columns in Excel: {', '.join(missing_cols)}")
    st.stop()

# Build dropdown options: "Item - Item Description"
df['search_label'] = df['Item'].astype(str).str.strip() + " - " + df['Item Description'].astype(str).str.strip()
search_map = dict(zip(df['search_label'], df['Item']))

# Dropdown + Clear Button inline
st.markdown("#### Select Item:")
col1, col2 = st.columns([5, 1])

options = [""] + sorted(search_map.keys())  # Include blank first entry for clear/reset

with col1:
    selected_label = st.selectbox(
        label="",
        options=options,
        key="item_select",
        label_visibility="collapsed"
    )

with col2:
    st.markdown(" ")  # visual spacer
    if st.button("Clear"):
        st.session_state["item_select"] = options[0]  # Reset to blank
        st.experimental_rerun()

# Only process if something is selected
if selected_label:
    selected_item = search_map[selected_label]

    matches = df[df['Item'].astype(str).str.strip().str.lower() == selected_item.strip().lower()]

    if not matches.empty:
        st.success(f"Found {len(matches)} matching bin(s):")

        # Sort by Bin Location Description and hide index
        table = matches[['Bin Location Description', 'Item Qty']].copy()
        table = table.sort_values(by='Bin Location Description')
        table.index = [''] * len(table)  # Hide index

        st.table(table)
    else:
        st.warning("Item not found.")

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

# User selects from dropdown
selected_label = st.selectbox("Select Item:", options=sorted(search_map.keys()))

# Get actual Item from label
selected_item = search_map[selected_label]

# Filter and show results
matches = df[df['Item'].astype(str).str.strip().str.lower() == selected_item.strip().lower()]

if not matches.empty:
    st.success(f"Found {len(matches)} matching bin(s):")
    st.dataframe(
    matches[['Bin Location Description', 'Item Qty']],
    use_container_width=True,
    hide_index=True
)
else:
    st.warning("Item not found.")

import streamlit as st
import pandas as pd

# Load and clean the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('C:\\Users\\lab305\\Desktop\\cahmp\\cahmp\\food1.csv')
    df.columns = df.columns.str.strip()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

df = load_data()

# Utility for price parsing
def parse_price(price_str):
    prices = [int(p.replace('₹', '').strip()) for p in price_str.split('-')]
    return prices[0], prices[1]

# App Title
st.title("🍽️ Indian Food Recommender")

# Model Selector
model_type = st.sidebar.selectbox("Choose Recommendation Type", [
    "By State & Festival",
    "By Season (Time)",
    "By Diet Type",
    "By Spice Level",
    "By Price Range"
])

# Model 1: By State & Festival
if model_type == "By State & Festival":
    state = st.selectbox("Select State", sorted(df['State'].unique()))
    festival = st.selectbox("Select Festival", sorted(df['Festival'].unique()))
    result = df[(df['State'] == state) & (df['Festival'] == festival)]
    st.dataframe(result)

# Model 2: By Season
elif model_type == "By Season (Time)":
    season = st.selectbox("Select Season", sorted(df['Season'].unique()))
    result = df[df['Season'].str.contains(season, case=False)]
    st.dataframe(result)

# Model 3: By Diet Type
elif model_type == "By Diet Type":
    diet_type = st.selectbox("Select Diet Type", sorted(df['Diet_Type'].unique()))
    result = df[df['Diet_Type'].str.lower() == diet_type.lower()]
    st.dataframe(result)

# Model 4: By Spice Level
elif model_type == "By Spice Level":
    spice_level = st.selectbox("Select Spice Level", sorted(df['Spice_Level'].unique()))
    result = df[df['Spice_Level'].str.lower() == spice_level.lower()]
    st.dataframe(result)

# Model 5: By Price Range
elif model_type == "By Price Range":
    min_price = st.slider("Minimum Price (₹)", 50, 500, 100)
    max_price = st.slider("Maximum Price (₹)", 100, 1000, 300)

    recommendations = []
    for _, row in df.iterrows():
        low, high = parse_price(row['Price_Range'])
        if low >= min_price and high <= max_price:
            recommendations.append(row)
    result = pd.DataFrame(recommendations)
    st.dataframe(result)

# Footer
st.markdown("---")
st.markdown("🔍 _Explore regional, seasonal, and dietary food delights from India_ 🇮🇳")

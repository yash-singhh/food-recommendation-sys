import streamlit as st
import pandas as pd
import numpy as np
import datetime
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

# Download NLTK data
nltk.download('punkt')

# Festival-Based Food Recommendations
festival_meals = {
    "Lohri": {"Punjab": ["Lassi", "Sarson da Saag", "Makki di Roti"]},
    "Diwali": {"Gujarat": ["Kaju Katli", "Fafda Jalebi"], "Maharashtra": ["Modak", "Puran Poli"]},
    "Onam": {"Kerala": ["Onam Sadya", "Avial", "Payasam"]}
}

# Sample Dataset
data = {
    'State': ['Gujarat', 'Maharashtra', 'Punjab', 'West Bengal', 'Tamil Nadu'],
    'Food_Item': ['Dhokla', 'Pav Bhaji', 'Butter Chicken', 'Rasgulla', 'Dosa'],
    'Category': ['Vegetarian', 'Vegetarian', 'Non-Vegetarian', 'Dessert', 'Vegetarian'],
    'Spice_Level': ['Medium', 'High', 'High', 'Low', 'Medium'],
    'Season': ['All', 'All', 'Winter', 'Summer', 'All']
}

df = pd.DataFrame(data)

# Encode Features
encoder = LabelEncoder()
df['State_Enc'] = encoder.fit_transform(df['State'])
df['Food_Enc'] = encoder.fit_transform(df['Food_Item'])
df['Category_Enc'] = encoder.fit_transform(df['Category'])
df['Spice_Enc'] = encoder.fit_transform(df['Spice_Level'])
df['Season_Enc'] = encoder.fit_transform(df['Season'])

# Compute Similarity
features = df[['State_Enc', 'Category_Enc', 'Spice_Enc', 'Season_Enc']]
similarity_matrix = cosine_similarity(features)

# Food Recommendation Function
def recommend_food(state):
    idx = df[df['State'] == state].index[0]
    scores = sorted(enumerate(similarity_matrix[idx]), key=lambda x: x[1], reverse=True)
    recommended_foods = [df.iloc[i[0]]['Food_Item'] for i in scores[1:3]]
    return recommended_foods

# Festival Detector
def check_festival(state):
    today = datetime.datetime.today().strftime('%d-%m')
    for festival, regions in festival_meals.items():
        if state in regions and today in ["13-01", "14-01", "04-11"]:  # Lohri, Diwali, Onam
            return festival, regions[state]
    return None, None

# Chatbot for Customization
def chatbot_response(user_input):
    tokens = nltk.word_tokenize(user_input.lower())
    if "spicy" in tokens:
        return "We will make your meal spicier 🌶️!"
    elif "less oil" in tokens:
        return "We will prepare your meal with less oil 🥗!"
    else:
        return "Customization noted! ✅"

# Streamlit UI
def main():
    st.title("🍛 AI-Based Indian Food Recommendation System")

    # User selects state
    state_selected = st.selectbox("Select Your State:", df['State'].unique())

    # Check for festival-based recommendation
    festival, festival_foods = check_festival(state_selected)
    if festival:
        st.markdown(f"🎉 **{festival} Special Offer - 10% OFF** 🎉")
        st.success(f"Since it's {festival}, enjoy these recommended dishes: {', '.join(festival_foods)}")

    # Normal food recommendation
    recommendations = recommend_food(state_selected)
    st.success(f"🥘 Recommended foods for {state_selected}: {', '.join(recommendations)}")

    # Chatbot for customization
    st.subheader("🗣️ Customize Your Meal")
    user_input = st.text_input("Tell us how you'd like to customize your meal (e.g., Make it spicier)")
    if user_input:
        response = chatbot_response(user_input)
        st.write(response)

# Run the Streamlit App
if __name__ == '__main__':
    main()

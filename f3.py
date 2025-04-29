import streamlit as st
import pandas as pd
import datetime
import nltk
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import os

# Download NLTK tokenizer if not already present
nltk.download('punkt')

# 📌 Festival-Based Food Recommendations with Images
festival_meals = {
    "Lohri": {
        "Punjab": {
            "meals": ["Lassi", "Sarson da Saag", "Makki di Roti"],
            "image": "lohri_food.jpg",
            "price_range": "₹150 - ₹300"
        }
    },
    "Diwali": {
        "Gujarat": {
            "meals": ["Kaju Katli", "Fafda Jalebi"],
            "image": "diwali_food.jpg",
            "price_range": "₹200 - ₹400"
        },
        "Maharashtra": {
            "meals": ["Modak", "Puran Poli"],
            "image": "diwali_food.jpg",
            "price_range": "₹250 - ₹450"
        },
        "Punjab": {
            "meals": ["Besan Ladoo", "Pinni"],
            "image": "diwali_food.jpg",
            "price_range": "₹180 - ₹350"
        }
    }
}

# 📌 Festival Dates (DD-MM)
festival_dates = {
    "New Year": "01-01",
    "Lohri": "13-01",
    "Makar Sankranti": "14-01",
    "Republic Day": "26-01",
    "Shivaji Jayanti": "19-02",
    "International Women's Day": "08-03",
    "Holi": "25-03",
    "Ram Navami": "29-03",
    "Ugadi": "09-04",
    "Gudi Padwa": "10-04",
    "Baisakhi": "14-04",
    "Mahavir Jayanti": "21-04",
    "Buddha Purnima": "23-05",
    "Eid al-Adha": "17-06",
    "Independence Day": "15-08",
    "Raksha Bandhan": "19-08",
    "Janmashtami": "26-08",
    "Teacher's Day": "05-09",
    "Ganesh Chaturthi": "07-09",
    "Onam": "10-09",
    "Gandhi Jayanti": "02-10",
    "Durga Ashtami": "12-10",
    "Navami": "13-10",
    "Dussehra": "14-10",
    "Halloween": "31-10",
    "Karva Chauth": "01-11",
    "Diwali": "04-11",
    "Bhai Dooj": "08-11",
    "Christmas Eve": "24-12",
    "Christmas": "25-12"
}



# 📌 Load Food Dataset from CSV
file_path = "C:\\Users\\lab305\\Desktop\\cahmp\\cahmp\\food.csv"  # Adjust this path if necessary
if not os.path.exists(file_path):
    st.error(f"❌ 'food.csv' not found. Please upload the file in the working directory.")
    st.stop()

df = pd.read_csv(file_path)

# ✅ Validate required columns
required_cols = {'State', 'Food_Item', 'Category', 'Spice_Level', 'Season', 'Price_Range'}
if not required_cols.issubset(df.columns):
    st.error(f"❌ 'food.csv' must contain columns: {', '.join(required_cols)}")
    st.stop()

# 🔠 Label Encode for ML Similarity
encoder = LabelEncoder()
df['State_Enc'] = encoder.fit_transform(df['State'])
df['Food_Enc'] = encoder.fit_transform(df['Food_Item'])
df['Category_Enc'] = encoder.fit_transform(df['Category'])
df['Spice_Enc'] = encoder.fit_transform(df['Spice_Level'])
df['Season_Enc'] = encoder.fit_transform(df['Season'])

features = df[['State_Enc', 'Category_Enc', 'Spice_Enc', 'Season_Enc']]
similarity_matrix = cosine_similarity(features)

# 📌 Recommend Normal Foods
def recommend_food(state, price_range):
    filtered_df = df[(df['State'] == state) & (df['Price_Range'] == price_range)]
    if not filtered_df.empty:
        return list(filtered_df['Food_Item'])
    return ["No matching food items found for the selected price range"]

# 📌 Check Festival Special Meals
def check_festival(state, selected_date):
    festival = festival_dates.get(selected_date)
    if festival and state in festival_meals.get(festival, {}):
        return (
            festival,
            festival_meals[festival][state]["meals"],
            festival_meals[festival][state]["image"],
            festival_meals[festival][state]["price_range"]
        )
    return None, None, None, None

# 📌 Simple Customization Chatbot
def chatbot_response(user_input):
    tokens = nltk.word_tokenize(user_input.lower())
    if "spicy" in tokens:
        return "🔥 We will make your meal spicier!"
    elif "less oil" in tokens:
        return "🥗 We will prepare your meal with less oil!"
    elif "extra sweet" in tokens:
        return "🍯 Your meal will be extra sweet!"
    else:
        return "✅ Customization noted!"

# 📌 Show Main Page
def show_main_page():
    st.title("🍛 AI-Based Indian Food Recommendation System")

    state_selected = st.selectbox("📍 Select Your State:", df['State'].unique())
    price_range_selected = st.selectbox("💰 Select Price Range:", df['Price_Range'].unique())
    selected_date = st.text_input("📅 Enter a date (DD-MM) to test festival recommendations:", datetime.datetime.today().strftime('%d-%m'))
    cooking_style = st.radio("👨‍🍳 Choose Cooking Style:", ["As per User Preference", "Chef's Recommendation"])

    # Check festival
    festival, festival_foods, festival_image, festival_price_range = check_festival(selected_date,state_selected)

    if festival:
        st.markdown(f"🎉 **{festival} Special Offer - 10% OFF** 🎉")
        st.success(f"Since it's **{festival}**, enjoy these festival meals: 🍽️ {', '.join(festival_foods)} (Price Range: {festival_price_range})")
        try:
            image = Image.open(festival_image)
            st.image(image, caption=f"{festival} Special Meal", use_column_width=True)
        except:
            st.warning("🍽️ Festival meal image not found!")

    # Show regular food suggestions
    recommendations = recommend_food(state_selected, price_range_selected)
    st.success(f"🥘 Recommended foods for {state_selected} (Price Range: {price_range_selected}): {', '.join(recommendations)}")

    if festival:
        st.markdown("🎊 **Festival Special Discount: 10% OFF on all meals today!** 🎊")

    # Meal customization
    st.subheader("🗣️ Customize Your Meal")
    user_input = st.text_input("Tell us how you'd like to customize your meal (e.g., Make it spicier)")
    if user_input:
        response = chatbot_response(user_input)
        st.write(response)

    st.info(f"👨‍🍳 Your meal will be prepared: **{cooking_style}**")

# 📌 Show Festival Finder Page

# def show_festival_filter_page():
#     st.title("📅 Festival-Based Food Filter")

#     # Select festival from dropdown, populated by festivals in `festival_dates`
#     selected_festival = st.selectbox("🎊 Choose a Festival:", list(festival_dates.values()))

#     # Find the states for the selected festival
#     states_for_festival = []
#     for festival, states in festival_meals.items():
#         if festival_dates.get(selected_festival[:5], None) == festival:  # Match festival name
#             states_for_festival.extend(states.keys())  # Add all states related to the selected festival

#     # Remove duplicates and ensure unique states are shown in dropdown
#     available_states = list(set(states_for_festival))

#     if available_states:
#         selected_state = st.selectbox("📍 Choose State:", available_states)

#         # Display meals for the selected festival and state
#         if selected_festival in festival_meals and selected_state in festival_meals[selected_festival]:
#             meal_info = festival_meals[selected_festival][selected_state]
#             st.success(f"🍽️ Special meals for {selected_festival} in {selected_state}: {', '.join(meal_info['meals'])} (Price Range: {meal_info['price_range']})")

#             # Show image for the festival meal
#             try:
#                 image = Image.open(meal_info['image'])
#                 st.image(image, caption=f"{selected_festival} Special", use_column_width=True)
#             except Exception as e:
#                 st.warning("⚠️ Image for this festival meal not found.")
#     else:
#         st.error("No available states for the selected festival.")

def show_festival_filter_page():
    st.title("📅 Festival-Based Food Filter")

    # Select festival from dropdown
    selected_festival = st.selectbox("🎊 Choose a Festival:", list(festival_meals.keys()))

    # Filter available states for that festival
    available_states = list(festival_meals[selected_festival].keys())
    selected_state = st.selectbox("📍 Choose State:", available_states)

    # Display meals
    meal_info = festival_meals[selected_festival][selected_state]
    st.success(f"🍽️ Special meals for {selected_festival} in {selected_state}: {', '.join(meal_info['meals'])} (Price Range: {meal_info['price_range']})")

    # Show image
    try:
        image = Image.open(meal_info['image'])
        st.image(image, caption=f"{selected_festival} Special", use_column_width=True)
    except:
        st.warning("⚠️ Image for this festival meal not found.")

# 📌 Run the app with page navigation
if __name__ == "__main__":
    st.sidebar.title("🔀 Navigate")
    page = st.sidebar.radio("Go to", ["🏠 Home", "🎯 Festival Finder"])

    if page == "🏠 Home":
        show_main_page()
    elif page == "🎯 Festival Finder":
        show_festival_filter_page()

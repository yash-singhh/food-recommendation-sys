# 🍛 Indian Food Recommendation System

An interactive **Streamlit** application that recommends Indian dishes based on various user preferences like state, festival, season, spice level, diet type, and budget. This project explores India’s culinary diversity with contextual insights for each dish.

---

## 🔍 Features

- 🎉 **State & Festival-Based Recommendations**  
  Suggests foods traditionally prepared in different Indian states during festivals.

- ☀️ **Season-Based Suggestions**  
  Find dishes suitable for Winter, Summer, or Monsoon.

- 🥦 **Diet Type Filter**  
  Choose between Vegetarian, Vegan, or Non-Vegetarian food.

- 🌶️ **Spice Level Selector**  
  Filter based on your spice tolerance: Low, Medium, or High.

- 💰 **Budget-Based Food Discovery**  
  Customize recommendations based on your spending range.

- 📖 **Detailed Descriptions**  
  Each dish includes background, ingredients, and cultural relevance.

---

## 🗃️ Dataset

The application uses a CSV file (`food1.csv`) with the following columns:

- `State`
- `Food_Item`
- `Category`
- `Spice_Level`
- `Season`
- `Price_Range`
- `Diet_Type`
- `Festival`
- `Description` *(added manually)*

You can expand the dataset to include more regions, festivals, or add image URLs.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/indian-food-recommender.git
cd indian-food-recommender
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Run the Streamlit App
bash
Copy
Edit
streamlit run app.py
📁 File Structure
bash
Copy
Edit
.
├── app.py               # Main Streamlit application
├── food1.csv            # Dataset containing Indian food details
├── requirements.txt     # List of required Python libraries
└── README.md            # Project documentation
💡 Use Cases
Cultural food discovery platforms

Seasonal diet planners

Festival-specific meal suggestions

Educational or tourism-focused apps

🛠️ Built With
Python

Streamlit

Pandas

🙌 Contributing
Feel free to fork the repo, improve the dataset, add new recommendation modes, or enhance the UI with images and filters.

📜 License
This project is licensed under the MIT License. See LICENSE for details.

🇮🇳 Celebrate India, One Dish at a Time!
vbnet
Copy
Edit

Would you like me to generate the `requirements.txt` as well?

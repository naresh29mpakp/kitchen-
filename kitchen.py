import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import pandas as pd

# Placeholder image URL for unavailable images
placeholder_image_url = "https://via.placeholder.com/150"

# Kitchen Inventory Data
inventory = {
    "Vegetables": [
        {"name": "Tomatoes", "quantity": 20, "image_url": "https://upload.wikimedia.org/wikipedia/commons/8/89/Tomato_je.jpg"},
        {"name": "Carrots", "quantity": 15, "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Carrot.jpg"},
        {"name": "Onions", "quantity": 25, "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/91/Onion.jpg"},
        {"name": "Potatoes", "quantity": 30, "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Patates.jpg"},
        {"name": "Spinach", "quantity": 10, "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e2/Spinach_leaves.jpg"}
    ],
    "Fruits": [
        {"name": "Bananas", "quantity": 12, "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Bananas_white_background.jpg"},
        {"name": "Apples", "quantity": 8, "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg"},
        {"name": "Oranges", "quantity": 10, "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c4/Orange-Fruit-Pieces.jpg"},
        {"name": "Grapes", "quantity": 15, "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/36/Kyoho-grape.jpg"},
        {"name": "Mangoes", "quantity": 5, "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/90/Hapus_Mango.jpg"}
    ],
    "Grains": [
        {"name": "Rice", "quantity": 50, "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/65/Rice_closeup.jpg"},
        {"name": "Wheat", "quantity": 30, "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Wheat_close-up.JPG"},
        {"name": "Lentils", "quantity": 20, "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Lentils.jpg"},
        {"name": "Chickpeas", "quantity": 15, "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Chickpeas.jpg"},
        {"name": "Oats", "quantity": 10, "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/22/Oatmeal_bowl.jpg"}
    ],
    "Dairy": [
        {"name": "Milk", "quantity": 10, "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Milk_glass.jpg"},
        {"name": "Cheese", "quantity": 5, "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/33/Cheese.jpg"},
        {"name": "Yogurt", "quantity": 8, "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Greek_yogurt.jpg"},
        {"name": "Butter", "quantity": 6, "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Butter.jpg"},
        {"name": "Paneer", "quantity": 10, "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Paneer.jpg"}
    ],
    "Masala Powders": [
        {"name": "Turmeric Powder", "quantity": 5, "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Turmeric.jpg"},
        {"name": "Chili Powder", "quantity": 6, "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Chili_powder.jpg"},
        {"name": "Coriander Powder", "quantity": 4, "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Coriander_Powder.jpg"},
        {"name": "Garam Masala", "quantity": 3, "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/70/Garam_masala_powder.jpg"},
        {"name": "Cumin Powder", "quantity": 5, "image_url": "https://upload.wikimedia.org/wikipedia/commons/8/8b/Cumin_powder.jpg"}
    ],
    "Whole Masalas": [
        {"name": "Cumin Seeds", "quantity": 7, "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/35/Cumin_seeds.jpg"},
        {"name": "Mustard Seeds", "quantity": 8, "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/fc/Mustard_seeds.jpg"},
        {"name": "Fenugreek Seeds", "quantity": 6, "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Fenugreek_seeds.jpg"},
        {"name": "Black Pepper", "quantity": 10, "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Black_pepper.jpg"},
        {"name": "Cloves", "quantity": 4, "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Cloves.jpg"}
    ],
    "Greens (Keerai)": [
        {"name": "Spinach", "quantity": 10, "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e2/Spinach_leaves.jpg"},
        {"name": "Fenugreek Leaves", "quantity": 5, "image_url": "https://upload.wikimedia.org/wikipedia/commons/8/89/Fenugreek_leaves.jpg"},
        {"name": "Coriander Leaves", "quantity": 8, "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/Coriander_leaves.jpg"},
        {"name": "Mint Leaves", "quantity": 6, "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Mint_leaves.jpg"},
        {"name": "Drumstick Leaves", "quantity": 7, "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Drumstick_leaves.jpg"}
    ]
}

# Shopping List
shopping_list = []

def add_to_shopping_list(item_name):
    if item_name not in shopping_list:
        shopping_list.append(item_name)

def remove_from_shopping_list(item_name):
    if item_name in shopping_list:
        shopping_list.remove(item_name)

# Streamlit App
st.title("Kitchen Inventory Checklist")
st.write("Track your kitchen inventory by category with images and quantities. Add items to your shopping list as needed.")

for category, items in inventory.items():
    st.header(category)
    for item in items:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        # Display item image
        with col1:
            try:
                response = requests.get(item["image_url"])
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                else:
                    response = requests.get(placeholder_image_url)
                    image = Image.open(BytesIO(response.content))
                st.image(image, use_column_width=True)
            except Exception as e:
                response = requests.get(placeholder_image_url)
                image = Image.open(BytesIO(response.content))
                st.image(image, use_column_width=True)
        
        # Display item details
        with col2:
            st.subheader(item["name"])
            st.write(f"Quantity Available: {item['quantity']}")
        
        # Add/Remove buttons
        with col3:
            # Unique keys by combining category and item name
            if st.button(f"Add {item['name']}", key=f"add_{category}_{item['name']}"):
                add_to_shopping_list(item["name"])
            if st.button(f"Remove {item['name']}", key=f"remove_{category}_{item['name']}"):
                remove_from_shopping_list(item["name"])

# Display and Download Shopping List
st.header("Shopping List")
if shopping_list:
    for item in shopping_list:
        st.write(f"- {item}")
    csv = pd.DataFrame(shopping_list, columns=["Item"]).to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Shopping List", data=csv, file_name="shopping_list.csv", mime="text/csv")
else:
    st.write("Your shopping list is empty.")

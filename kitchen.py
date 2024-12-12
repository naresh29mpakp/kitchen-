import streamlit as st
import pandas as pd
from PIL import Image
import os

# Set up GitHub storage path
GITHUB_PATH = "https://raw.githubusercontent.com/naresh29mpakp/kitchen-/main/"
LOCAL_IMAGE_DIR = "images/"
os.makedirs(LOCAL_IMAGE_DIR, exist_ok=True)

# Helper function to save images locally and simulate upload to GitHub
def save_image(image_file, filename):
    image_path = os.path.join(LOCAL_IMAGE_DIR, filename)
    with open(image_path, "wb") as f:
        f.write(image_file.getbuffer())
    # Simulate uploading to GitHub (Replace with real upload logic if needed)
    return GITHUB_PATH + filename

# Title
st.title("Grocery Inventory Management")

# Sidebar Instructions
st.sidebar.header("Instructions")
st.sidebar.write("1. Add categories and upload images for them.")
st.sidebar.write("2. Add products with name, image, quantity, and category.")
st.sidebar.write("3. View products by selecting a category or on the home page.")

# Session state to manage categories and products
if 'categories' not in st.session_state:
    st.session_state.categories = {}
if 'products' not in st.session_state:
    st.session_state.products = []

# Home Page to display all categories
st.subheader("Home - All Categories")
cols = st.columns(3)
for idx, (category, image_url) in enumerate(st.session_state.categories.items()):
    with cols[idx % 3]:
        st.image(image_url, caption=category, use_column_width=True)

# Add a new category
st.subheader("Add a New Category")
category_name = st.text_input("Category Name:")
category_image = st.file_uploader("Upload Category Image:", type=["png", "jpg", "jpeg"])
if st.button("Add Category"):
    if category_name and category_image:
        saved_url = save_image(category_image, f"category_{category_name}.png")
        st.session_state.categories[category_name] = saved_url
        st.success(f"Category '{category_name}' added!")
    else:
        st.error("Please provide both a category name and an image.")

# Add a new product
st.subheader("Add a New Product")
product_name = st.text_input("Product Name:")
product_image = st.file_uploader("Upload Product Image:", type=["png", "jpg", "jpeg"], key="product_image")
product_quantity = st.number_input("Quantity Available:", min_value=1, step=1)
product_category = st.selectbox("Select Category:", ["Select"] + list(st.session_state.categories.keys()))
if st.button("Add Product"):
    if product_name and product_image and product_quantity > 0 and product_category != "Select":
        saved_url = save_image(product_image, f"product_{product_name}.png")
        st.session_state.products.append({
            "name": product_name,
            "image": saved_url,
            "quantity": product_quantity,
            "category": product_category
        })
        st.success(f"Product '{product_name}' added to category '{product_category}'!")
    else:
        st.error("Please fill in all fields to add a product.")

# View products by category
st.subheader("View Products by Category")
selected_category = st.selectbox("Select Category:", ["Select"] + list(st.session_state.categories.keys()), key="view_category")
if selected_category != "Select":
    st.write(f"Products in '{selected_category}'")
    product_cols = st.columns(3)
    for idx, product in enumerate(st.session_state.products):
        if product["category"] == selected_category:
            with product_cols[idx % 3]:
                st.image(product["image"], caption=f"{product['name']} (Qty: {product['quantity']})", width=200)

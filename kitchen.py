import streamlit as st
import pandas as pd
from PIL import Image

# Title
st.title("Grocery Inventory Management")

# Sidebar Instructions
st.sidebar.header("Instructions")
st.sidebar.write("1. Add categories and upload images for them.")
st.sidebar.write("2. Add products with name, image, quantity, and category.")
st.sidebar.write("3. View products by selecting a category.")

# Session state to manage categories and products
if 'categories' not in st.session_state:
    st.session_state.categories = {}
if 'products' not in st.session_state:
    st.session_state.products = []

# Add a new category
st.subheader("Add a New Category")
category_name = st.text_input("Category Name:")
category_image = st.file_uploader("Upload Category Image:", type=["png", "jpg", "jpeg"])
if st.button("Add Category"):
    if category_name and category_image:
        category_image = Image.open(category_image)
        st.session_state.categories[category_name] = category_image
        st.success(f"Category '{category_name}' added!")
    else:
        st.error("Please provide both a category name and an image.")

# Display categories
st.subheader("Available Categories")
for category, image in st.session_state.categories.items():
    st.image(image, caption=category, use_column_width=True)

# Add a new product
st.subheader("Add a New Product")
product_name = st.text_input("Product Name:")
product_image = st.file_uploader("Upload Product Image:", type=["png", "jpg", "jpeg"], key="product_image")
product_quantity = st.number_input("Quantity Available:", min_value=1, step=1)
product_category = st.selectbox("Select Category:", ["Select"] + list(st.session_state.categories.keys()))
if st.button("Add Product"):
    if product_name and product_image and product_quantity > 0 and product_category != "Select":
        product_image = Image.open(product_image)
        st.session_state.products.append({
            "name": product_name,
            "image": product_image,
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
    for product in st.session_state.products:
        if product["category"] == selected_category:
            st.image(product["image"], caption=f"{product['name']} (Qty: {product['quantity']})", use_column_width=True)

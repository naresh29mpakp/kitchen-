import streamlit as st
import pandas as pd
import os
import json
from PIL import Image
import base64

# Set up directories
GITHUB_PATH = "https://raw.githubusercontent.com/naresh29mpakp/kitchen-/main/"
LOCAL_IMAGE_DIR = "images/"
DATA_FILE = "data.json"
os.makedirs(LOCAL_IMAGE_DIR, exist_ok=True)

# Load saved data from JSON
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        saved_data = json.load(f)
    categories = saved_data.get("categories", {})
    products = saved_data.get("products", [])
else:
    categories = {}
    products = []

# Save data to JSON
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"categories": categories, "products": products}, f)

# Helper function to save images locally and simulate upload to GitHub
def save_image(image_file, filename):
    image_path = os.path.join(LOCAL_IMAGE_DIR, filename)
    with open(image_path, "wb") as f:
        f.write(image_file.getbuffer())
    return GITHUB_PATH + filename

# Page routing
page = st.sidebar.selectbox("Navigate", ["Product Categories", "Add Categories and Products"])

# Session states for inventory list
if "inventory_list" not in st.session_state:
    st.session_state.inventory_list = []

# Product Categories Page
if page == "Product Categories":
    st.title("Product Categories")

    # Display categories
    st.subheader("Browse Categories")
    if categories:
        cols = st.columns(3)
        for idx, (category, image_url) in enumerate(categories.items()):
            with cols[idx % 3]:
                if st.button(category):
                    st.session_state.selected_category = category
    else:
        st.info("No categories available. Please add categories on the other page.")

    # Display products in selected category
    if "selected_category" in st.session_state:
        st.subheader(f"Products in {st.session_state.selected_category}")
        category_products = [p for p in products if p["category"] == st.session_state.selected_category]
        if category_products:
            product_cols = st.columns(3)
            for idx, product in enumerate(category_products):
                with product_cols[idx % 3]:
                    st.image(product["image"], caption=product["name"], width=200)
                    if st.button(f"Add {product['name']} to Inventory", key=f"add_{product['name']}"):
                        st.session_state.inventory_list.append(product)
                    if st.button(f"Remove {product['name']} from Inventory", key=f"remove_{product['name']}"):
                        if product in st.session_state.inventory_list:
                            st.session_state.inventory_list.remove(product)
        else:
            st.info("No products available in this category.")

    # View Inventory List
    if st.button("View Inventory List"):
        st.subheader("Inventory Restock List")
        if st.session_state.inventory_list:
            inventory_df = pd.DataFrame(st.session_state.inventory_list)
            st.table(inventory_df["name"])

            # Generate WhatsApp share link
            inventory_text = ", ".join(inventory_df["name"].tolist())
            share_url = f"https://wa.me/?text=Inventory Restock List: {inventory_text}"
            st.markdown(f"[Share on WhatsApp]({share_url})")
        else:
            st.info("Inventory list is empty.")

# Add Categories and Products Page
elif page == "Add Categories and Products":
    st.title("Add Categories and Products")

    # Add Category
    st.subheader("Add a New Category")
    category_name = st.text_input("Category Name:")
    category_image = st.file_uploader("Upload Category Image:", type=["png", "jpg", "jpeg"], key="category_image")
    if st.button("Add Category"):
        if category_name and category_image:
            saved_url = save_image(category_image, f"category_{category_name}.png")
            categories[category_name] = saved_url
            save_data()
            st.success(f"Category '{category_name}' added!")
        else:
            st.error("Please provide both a category name and an image.")

    # Add Product
    st.subheader("Add a New Product")
    product_name = st.text_input("Product Name:", key="product_name")
    product_image = st.file_uploader("Upload Product Image:", type=["png", "jpg", "jpeg"], key="product_image")
    product_category = st.selectbox("Select Category:", ["Select"] + list(categories.keys()))
    if st.button("Add Product"):
        if product_name and product_image and product_category != "Select":
            saved_url = save_image(product_image, f"product_{product_name}.png")
            products.append({
                "name": product_name,
                "image": saved_url,
                "category": product_category
            })
            save_data()
            st.success(f"Product '{product_name}' added to category '{product_category}'!")
        else:
            st.error("Please fill in all fields to add a product.")

import streamlit as st
import pandas as pd

# Title
st.title("Grocery Inventory Management")

# Sidebar Instructions
st.sidebar.header("Instructions")
st.sidebar.write("1. Add items to your grocery list.")
st.sidebar.write("2. Remove items if needed.")
st.sidebar.write("3. Download your final list as a .txt file.")

# Default inventory
inventory = ["Rice", "Wheat", "Sugar", "Salt", "Milk", "Eggs", "Bread", "Butter"]

# Session state to manage the list
if 'grocery_list' not in st.session_state:
    st.session_state.grocery_list = inventory.copy()

# Display inventory
st.subheader("Available Items")
st.write(inventory)

# Add items to the grocery list
st.subheader("Add Items to Your Grocery List")
new_item = st.text_input("Enter an item to add:")
if st.button("Add Item"):
    if new_item:
        st.session_state.grocery_list.append(new_item)
        st.success(f"'{new_item}' added to the list!")
    else:
        st.error("Please enter an item name.")

# Remove items from the grocery list
st.subheader("Remove Items from Your Grocery List")
remove_item = st.selectbox("Select an item to remove:", st.session_state.grocery_list)
if st.button("Remove Item"):
    st.session_state.grocery_list.remove(remove_item)
    st.success(f"'{remove_item}' removed from the list!")

# Display current grocery list
st.subheader("Your Grocery List")
st.write(st.session_state.grocery_list)

# Download the list as a .txt file
st.subheader("Download Your List")
if st.button("Download as .txt"):
    grocery_list_text = "\n".join(st.session_state.grocery_list)
    st.download_button(
        label="Download Grocery List",
        data=grocery_list_text,
        file_name="grocery_list.txt",
        mime="text/plain",
    )

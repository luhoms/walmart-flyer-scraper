import streamlit as st
import pandas as pd

df = pd.read_csv("walmart_flyer.csv")

st.title("Walmart Weekly Flyer")

search = st.text_input("Search for item: ")

if search:
    df = df[df["item"].str.contains(search, case=False, na=False)]

max_price = st.slider("Max price", 0.0, 100.0, 10.0)
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df = df[df["price"] <= max_price]

df["link"] = df["link"].apply(
    lambda url: f"[View Item]({url})" if pd.notna(url) and str(url).strip() else "Not Avaliable")

df.rename(columns={
    "item": "Item Name", 
    "price": "Price",
    "link": "Product Link"
}, inplace=True)

st.markdown(df[["Item Name", "Price", "Product Link"]].to_markdown(index=False), unsafe_allow_html=True)
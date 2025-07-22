import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="P2P Penny to Platinum", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #FFD700; }
    </style>
""", unsafe_allow_html=True)

st.image("assets/logo.png", width=180)
st.title("🏆 P2P Penny to Platinum - Card Collection Viewer")

url = "https://www.sportscardspro.com/offers?seller=d4vqzkmy5y6loajwxdlq7367za&status=collection"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
tables = pd.read_html(response.text)

if tables:
    df = tables[0]
    image_tags = soup.select("table img")
    image_urls = [img["src"] for img in image_tags]
    df["Image URL"] = image_urls

    search = st.text_input("Search your collection")

    filtered = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)] if search else df

    for i, row in filtered.iterrows():
        st.markdown("----")
        cols = st.columns([1, 3])
        with cols[0]:
            st.image(row["Image URL"], width=100)
        with cols[1]:
            st.subheader(str(row.get("Card", "Card")))
            st.write(f"**Price:** {row.get('Price', 'N/A')}")
else:
    st.warning("No table found on the page.")

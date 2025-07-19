# app.py

import streamlit as st
from src.services.web_scraper import WebScraper

# --- Streamlit UI ---

st.title("📄 Web Scraper for Job Postings")
st.info("Enter the URL of a job posting to extract its text content. Note that scraping can take a few moments.")

# Use caching to keep a single instance of the scraper


@st.cache_resource
def get_scraper():
    return WebScraper()


scraper = get_scraper()

# Create the UI elements
url = st.text_input("Enter Job Post URL:",
                    placeholder="https://example.com/job/123")

if st.button("Scrape and Extract Text"):
    if url:
        with st.spinner("Scraping in progress... Please wait."):
            extracted_text = scraper.scrape_text_from_url(url)
            st.subheader("✅ Extracted Text")
            st.text_area("Scraped Content", extracted_text, height=400)
    else:
        st.warning("Please enter a URL first.")

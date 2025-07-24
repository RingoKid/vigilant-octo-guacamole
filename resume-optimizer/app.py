# app.py

import streamlit as st
from src.chains import get_analyzer_chain

# --- Streamlit UI ---

st.title("📄 Job Post Text Analyzer")
st.info("Paste the text of a job posting below to analyze its content. No URL required.")

# --- Job Description Analyzer UI ---
st.header("🔍 Job Description Analyzer")
job_description = st.text_area(
    "Paste a job description to analyze:", height=200)

if st.button("Analyze Job Description"):
    if job_description:
        with st.spinner("Analyzing job description..."):
            chain = get_analyzer_chain()
            result = chain.invoke({"job_description": job_description})
            st.subheader("Analysis Result (JSON)")
            st.json(result)
    else:
        st.warning("Please paste a job description first.")

# # Use caching to keep a single instance of the scraper
#
# @st.cache_resource
# def get_scraper():
#     return WebScraper()
#
# scraper = get_scraper()
#
# # Create the UI elements
# url = st.text_input("Enter Job Post URL:",
#                     placeholder="https://example.com/job/123")
#
# if st.button("Scrape and Extract Text"):
#     if url:
#         with st.spinner("Scraping in progress... Please wait."):
#             extracted_text = scraper.scrape_text_from_url(url)
#             st.subheader("✅ Extracted Text")
#             st.text_area("Scraped Content", extracted_text, height=400)
#     else:
#         st.warning("Please enter a URL first.")

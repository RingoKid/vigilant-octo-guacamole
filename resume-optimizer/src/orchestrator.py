from src.services.ai_engine import AIEngine
from src.services.web_scraper import WebScraper
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


class Orchestrator:
    def __init__(self):
        self.scraper = WebScraper()
        self.ai_engine = AIEngine()

    def run(self):
        st.title("📄 Job Description Analyzer")
        st.info("Enter a job post URL to scrape, or paste a raw job description. If both are provided, the URL will be used.")

        url = st.text_input("Enter Job Post URL:",
                            placeholder="https://example.com/job/123")
        raw_text = st.text_area("Or paste Raw Job Description:", height=200)

        if st.button("Analyze Job Description"):
            job_text = None
            if url:
                with st.spinner("Scraping in progress... Please wait."):
                    job_text = self.scraper.scrape_text_from_url(url)
            elif raw_text.strip():
                job_text = raw_text.strip()
            else:
                st.warning(
                    "Please provide either a URL or raw job description text.")
                return

            if job_text:
                st.subheader("✅ Job Description Text")
                st.text_area("Job Description", job_text, height=300)
                with st.spinner("Extracting keywords using AI..."):
                    keywords = self.ai_engine.get_keywords(job_text)
                st.subheader("🔑 Extracted Keywords")
                st.write(", ".join(keywords)
                         if keywords else "No keywords found.")
            else:
                st.warning("Failed to retrieve job description text.")

# app.py

import streamlit as st
from src.chains import get_analyzer_chain, get_rewriter_chain
from src.parsers import JobDescriptionKeywords

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

# --- Resume Rewriter UI ---
st.header("✏️ Resume Rewriter")
st.info("Use the example resume and keywords to see how the rewriter chain works.")

if st.button("Run Resume Rewriter Example"):
    with st.spinner("Processing resume with example keywords..."):
        try:
            # Create a custom version of example_usage that returns results instead of printing
            rewriter_chain = get_rewriter_chain()

            # Read the resume from file
            with open("/workspaces/agents/resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
                resume_text = file.read()

            # Define keywords using JobDescriptionKeywords format
            job_keywords = JobDescriptionKeywords(
                technical_skills=["Design and build features", "build distributed platforms at scale",
                                  "algorithms", "data structures", "customer-facing product development",
                                  "building large-scale systems"],
                technologies_and_tools=["Java", "Python", "SQL"],
                soft_skills=["Collaboration", "communication"],
                certifications=[],
                other_requirements=["2-5 years' of industry experience",
                                    "Strong fundamental computer science skills",
                                    "BS/MS/PhD in Computer Science or related majors, or equivalent experience"]
            )

            # Flatten all keywords into a single list for the rewriter chain
            all_keywords = (
                job_keywords.technical_skills +
                job_keywords.technologies_and_tools +
                job_keywords.soft_skills +
                job_keywords.certifications +
                job_keywords.other_requirements
            )

            # Call the rewriter chain
            result = rewriter_chain.invoke({
                "keywords_to_integrate": all_keywords,
                "original_resume_text": resume_text
            })

            st.subheader("🎯 Keywords Used (JobDescriptionKeywords Format)")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Technical Skills:**")
                st.write(", ".join(job_keywords.technical_skills))

                st.write("**Technologies & Tools:**")
                st.write(", ".join(job_keywords.technologies_and_tools))

                st.write("**Soft Skills:**")
                st.write(", ".join(job_keywords.soft_skills))

            with col2:
                st.write("**Certifications:**")
                st.write(", ".join(job_keywords.certifications)
                         if job_keywords.certifications else "None specified")

                st.write("**Other Requirements:**")
                st.write(", ".join(job_keywords.other_requirements))

            st.subheader("📝 Optimized Resume Content")

            st.write("**Updated Summary:**")
            st.write(result['updated_summary'])

            st.write("**Liberty Mutual Group Experience:**")
            for bullet in result['liberty_mutual_group']:
                st.write(f"• {bullet}")

            st.write("**Inovace Technologies Experience:**")
            for bullet in result['inovace_technologies']:
                st.write(f"• {bullet}")

            st.write("**Spider Digital Commerce Experience:**")
            for bullet in result['spider_digital_commerce']:
                st.write(f"• {bullet}")

            st.write("**Echo Project Experience:**")
            for bullet in result['echo_project']:
                st.write(f"• {bullet}")

        except Exception as e:
            st.error(f"Error processing resume: {e}")

# Add option to use custom keywords
st.subheader("🔧 Custom Keywords")
custom_keywords = st.text_area(
    "Enter custom keywords (comma-separated):",
    value="Python, AWS, Docker, Kubernetes, CI/CD, REST APIs, Machine Learning",
    height=100
)

if st.button("Rewrite with Custom Keywords"):
    if custom_keywords:
        with st.spinner("Processing resume with custom keywords..."):
            try:
                rewriter_chain = get_rewriter_chain()

                # Read the resume from file
                with open("/workspaces/agents/resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
                    resume_text = file.read()

                # Parse custom keywords
                keywords_list = [kw.strip()
                                 for kw in custom_keywords.split(",") if kw.strip()]

                # Call the rewriter chain
                result = rewriter_chain.invoke({
                    "keywords_to_integrate": keywords_list,
                    "original_resume_text": resume_text
                })

                st.subheader("🎯 Custom Keywords Used")
                st.write(", ".join(keywords_list))

                st.subheader("📝 Optimized Resume Content")
                st.json(result)

            except Exception as e:
                st.error(f"Error processing resume: {e}")
    else:
        st.warning("Please enter some keywords first.")

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

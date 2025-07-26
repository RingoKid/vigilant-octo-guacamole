# app.py

import streamlit as st
from src.chains import get_analyzer_chain, get_rewriter_chain
from src.parsers import JobDescriptionKeywords
from src.file_manager import save_job_analysis_result, save_resume_optimization_result, list_saved_files

# --- Streamlit UI ---

st.title("📄 Job Post Text Analyzer")
st.info("Paste the text of a job posting below to analyze its content. No URL required.")

# --- Job Description Analyzer UI ---
st.header("🔍 Job Description Analyzer")
job_description = st.text_area(
    "Paste a job description to analyze:", height=200)

if 'analyzed_keywords' not in st.session_state:
    st.session_state['analyzed_keywords'] = None
if 'keywords_for_rewrite' not in st.session_state:
    st.session_state['keywords_for_rewrite'] = None

if st.button("Analyze Job Description"):
    if job_description:
        with st.spinner("Analyzing job description..."):
            chain = get_analyzer_chain()
            result = chain.invoke({"job_description": job_description})
            st.subheader("Analysis Result (JSON)")
            st.json(result)
            st.session_state['analyzed_keywords'] = result

            # Save the analysis result
            try:
                saved_file_path = save_job_analysis_result(
                    job_description, result)
                st.success(
                    f"✅ Analysis saved to: {saved_file_path.split('/')[-1]}")
            except Exception as e:
                st.warning(f"Analysis completed but couldn't save file: {e}")
    else:
        st.warning("Please paste a job description first.")

# Show button to use analyzed keywords for resume rewrite
if st.session_state['analyzed_keywords']:
    if st.button("Use These Keywords for Resume Rewrite"):
        # Flatten all keywords into a single list
        keywords = []
        for key in [
                'technical_skills', 'technologies_and_tools', 'soft_skills', 'certifications', 'other_requirements']:
            keywords += st.session_state['analyzed_keywords'].get(key, [])
        st.session_state['keywords_for_rewrite'] = keywords
        st.success("Keywords loaded for resume rewrite!")
    st.write("**Extracted Keywords:**")
    st.json(st.session_state['analyzed_keywords'])

# Button to rewrite resume with analyzed keywords
if st.session_state['keywords_for_rewrite']:
    if st.button("Rewrite Resume with Analyzed Keywords"):
        with st.spinner("Processing resume with analyzed keywords..."):
            try:
                rewriter_chain = get_rewriter_chain()
                with open("/workspaces/agents/resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
                    resume_text = file.read()
                result = rewriter_chain.invoke({
                    "keywords_to_integrate": st.session_state['keywords_for_rewrite'],
                    "original_resume_text": resume_text
                })
                st.subheader("🎯 Analyzed Keywords Used")
                st.write(", ".join(st.session_state['keywords_for_rewrite']))
                st.subheader("📝 Optimized Resume Content")
                st.json(result)

                # Save the optimization result
                try:
                    saved_file_path = save_resume_optimization_result(
                        st.session_state['keywords_for_rewrite'],
                        resume_text,
                        result,
                        "job_analysis"
                    )
                    st.success(
                        f"✅ Optimization saved to: {saved_file_path.split('/')[-1]}")
                except Exception as e:
                    st.warning(
                        f"Optimization completed but couldn't save file: {e}")
            except Exception as e:
                st.error(f"Error processing resume: {e}")

# --- Custom Keywords Section ---
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
                with open("/workspaces/agents/resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
                    resume_text = file.read()
                keywords_list = [kw.strip()
                                 for kw in custom_keywords.split(",") if kw.strip()]
                result = rewriter_chain.invoke({
                    "keywords_to_integrate": keywords_list,
                    "original_resume_text": resume_text
                })
                st.subheader("🎯 Custom Keywords Used")
                st.write(", ".join(keywords_list))
                st.subheader("📝 Optimized Resume Content")
                st.json(result)

                # Save the optimization result
                try:
                    saved_file_path = save_resume_optimization_result(
                        keywords_list,
                        resume_text,
                        result,
                        "custom"
                    )
                    st.success(
                        f"✅ Optimization saved to: {saved_file_path.split('/')[-1]}")
                except Exception as e:
                    st.warning(
                        f"Optimization completed but couldn't save file: {e}")
            except Exception as e:
                st.error(f"Error processing resume: {e}")
    else:
        st.warning("Please enter some keywords first.")

# --- Example Usage Section (Moved Down) ---
st.header("🧑‍💻 Example: Resume Rewriter with Example Keywords")
st.info("Use the example resume and keywords to see how the rewriter chain works.")

if st.button("Run Resume Rewriter Example"):
    with st.spinner("Processing resume with example keywords..."):
        try:
            rewriter_chain = get_rewriter_chain()
            with open("/workspaces/agents/resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
                resume_text = file.read()
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
            all_keywords = (
                job_keywords.technical_skills +
                job_keywords.technologies_and_tools +
                job_keywords.soft_skills +
                job_keywords.certifications +
                job_keywords.other_requirements
            )
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

            # Save the optimization result
            try:
                saved_file_path = save_resume_optimization_result(
                    all_keywords,
                    resume_text,
                    result,
                    "example"
                )
                st.success(
                    f"✅ Example optimization saved to: {saved_file_path.split('/')[-1]}")
            except Exception as e:
                st.warning(f"Example completed but couldn't save file: {e}")
        except Exception as e:
            st.error(f"Error processing resume: {e}")

# --- Saved Files Management Section ---
st.header("📁 Saved Files Management")
st.info("View and manage previously generated files from both chains.")

# Create tabs for different file types
tab1, tab2 = st.tabs(["📊 Job Analysis Files", "📝 Resume Optimization Files"])

with tab1:
    st.subheader("Job Analysis Results")
    try:
        saved_files = list_saved_files("job_analysis")
        job_analysis_files = saved_files.get("job_analysis", [])

        if job_analysis_files:
            st.write(
                f"Found {len(job_analysis_files)} saved job analysis files:")
            for i, filename in enumerate(sorted(job_analysis_files, reverse=True)):
                with st.expander(f"📄 {filename}", expanded=False):
                    if st.button(f"Show Details", key=f"job_analysis_{i}"):
                        try:
                            from src.file_manager import load_saved_file
                            file_data = load_saved_file(
                                "job_analysis", filename)

                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Metadata:**")
                                st.json(file_data["metadata"])
                            with col2:
                                st.write("**Input Preview:**")
                                st.write(file_data["input"]
                                         ["job_description_preview"])

                            st.write("**Analysis Result:**")
                            st.json(file_data["output"]["analysis_result"])
                        except Exception as e:
                            st.error(f"Error loading file: {e}")
        else:
            st.info(
                "No job analysis files found. Analyze a job description to create your first file!")
    except Exception as e:
        st.error(f"Error listing job analysis files: {e}")

with tab2:
    st.subheader("Resume Optimization Results")
    try:
        saved_files = list_saved_files("resume_optimization")
        resume_opt_files = saved_files.get("resume_optimization", [])

        if resume_opt_files:
            st.write(
                f"Found {len(resume_opt_files)} saved resume optimization files:")
            for i, filename in enumerate(sorted(resume_opt_files, reverse=True)):
                with st.expander(f"📄 {filename}", expanded=False):
                    if st.button(f"Show Details", key=f"resume_opt_{i}"):
                        try:
                            from src.file_manager import load_saved_file
                            file_data = load_saved_file(
                                "resume_optimization", filename)

                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Metadata:**")
                                st.json(file_data["metadata"])
                                st.write("**Keywords Used:**")
                                st.write(
                                    ", ".join(file_data["input"]["keywords_used"]))
                            with col2:
                                st.write("**Keywords Source:**")
                                st.write(file_data["metadata"]
                                         ["keywords_source"])
                                st.write("**Keywords Count:**")
                                st.write(file_data["input"]["keywords_count"])

                            st.write("**Optimization Result:**")
                            result = file_data["output"]["optimization_result"]
                            if isinstance(result, dict):
                                st.write("**Updated Summary:**")
                                st.write(result.get('updated_summary', 'N/A'))

                                for section in ['liberty_mutual_group', 'inovace_technologies', 'spider_digital_commerce', 'echo_project']:
                                    if section in result and result[section]:
                                        st.write(
                                            f"**{section.replace('_', ' ').title()}:**")
                                        for bullet in result[section]:
                                            st.write(f"• {bullet}")
                            else:
                                st.json(result)
                        except Exception as e:
                            st.error(f"Error loading file: {e}")
        else:
            st.info(
                "No resume optimization files found. Run a resume optimization to create your first file!")
    except Exception as e:
        st.error(f"Error listing resume optimization files: {e}")

# Summary statistics
st.subheader("📈 Summary Statistics")
try:
    all_files = list_saved_files("all")
    total_job_analysis = len(all_files.get("job_analysis", []))
    total_resume_opt = len(all_files.get("resume_optimization", []))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Job Analysis Files", total_job_analysis)
    with col2:
        st.metric("Resume Optimization Files", total_resume_opt)
    with col3:
        st.metric("Total Files", total_job_analysis + total_resume_opt)
except Exception as e:
    st.error(f"Error calculating statistics: {e}")

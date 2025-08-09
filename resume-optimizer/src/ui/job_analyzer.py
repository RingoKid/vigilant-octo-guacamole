"""
Job Description Analyzer UI components
"""
import streamlit as st
from src.chains import get_analyzer_chain
from src.file_manager import save_job_analysis_result


def render_job_analyzer():
    """Render the job description analyzer section"""
    st.header("🔍 Job Description Analyzer")

    job_description = st.text_area(
        "Paste a job description to analyze:", height=200)

    if st.button("Analyze Job Description"):
        if job_description:
            _analyze_job_description(job_description)
        else:
            st.warning("Please paste a job description first.")

    _render_keywords_usage_section()


def _analyze_job_description(job_description):
    """Analyze job description and save results"""
    with st.spinner("Analyzing job description..."):
        chain = get_analyzer_chain()
        result = chain.invoke({"job_description": job_description})
        st.subheader("Analysis Result")
        st.json(result)
        st.session_state['analyzed_keywords'] = result

        # Save the analysis result
        try:
            saved_file_path = save_job_analysis_result(job_description, result)
            st.success(
                f"✅ Analysis saved to: {saved_file_path.split('/')[-1]}")
        except Exception as e:
            st.warning(f"Analysis completed but couldn't save file: {e}")


def _render_keywords_usage_section():
    """Render section for using analyzed keywords"""
    if st.session_state['analyzed_keywords']:
        if st.button("Use These Keywords for Resume Rewrite"):
            # Flatten all keywords into a single list
            keywords = []
            for key in ['technical_skills', 'technologies_and_tools', 'soft_skills']:
                keywords += st.session_state['analyzed_keywords'].get(key, [])
            st.session_state['keywords_for_rewrite'] = keywords
            st.success("Keywords loaded for resume rewrite!")

        # # Only show keywords if they haven't been loaded for rewrite yet
        # if not st.session_state['keywords_for_rewrite']:
        #     st.write("**Extracted Keywords:**")
        #     st.json(st.session_state['analyzed_keywords'])


def get_keywords_for_rewrite():
    """Get keywords that are ready for rewrite"""
    return st.session_state.get('keywords_for_rewrite')

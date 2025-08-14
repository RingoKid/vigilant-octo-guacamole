"""
Application utilities for the resume optimizer
"""
import streamlit as st


def initialize_app():
    """Initialize the Streamlit app with title and basic settings"""
    st.title("📄 AI Resume Optimizer")
    st.info(
        "🚀 **One-Click Solution**: Paste a job description and get an optimized resume instantly! "
        "Or use advanced options for step-by-step control.")


def initialize_all_session_state():
    """Initialize all session state variables"""
    # Job analysis session state
    if 'analyzed_keywords' not in st.session_state:
        st.session_state['analyzed_keywords'] = None
    if 'keywords_for_rewrite' not in st.session_state:
        st.session_state['keywords_for_rewrite'] = None

    # Resume generation session state
    if 'last_optimization_result' not in st.session_state:
        st.session_state['last_optimization_result'] = None
    if 'original_resume' not in st.session_state:
        st.session_state['original_resume'] = None
    if 'updated_resume_html' not in st.session_state:
        st.session_state['updated_resume_html'] = None
    if 'updated_resume_markdown' not in st.session_state:
        st.session_state['updated_resume_markdown'] = None

    # PDF download session state
    if 'generated_pdf_path' not in st.session_state:
        st.session_state['generated_pdf_path'] = None
    if 'example_pdf_path' not in st.session_state:
        st.session_state['example_pdf_path'] = None
    if 'streamlined_pdf_path' not in st.session_state:
        st.session_state['streamlined_pdf_path'] = None


def get_resume_path():
    """Get the path to the resume file"""
    return "resume-optimizer/src/docs/resume.md"


def load_resume_text():
    """Load resume text from file"""
    with open(get_resume_path(), "r", encoding="utf-8") as file:
        return file.read()


def show_error_message(error, context=""):
    """Show standardized error message"""
    error_msg = f"Error {context}: {error}" if context else f"Error: {error}"
    st.error(error_msg)


def show_success_message(message):
    """Show standardized success message"""
    st.success(f"✅ {message}")


def show_warning_message(message):
    """Show standardized warning message"""
    st.warning(message)


def show_info_message(message):
    """Show standardized info message"""
    st.info(message)

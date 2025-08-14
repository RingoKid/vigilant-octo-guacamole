"""
Refactored Resume Optimizer Streamlit App

This is the main entry point for the resume optimization application.
The app has been modularized for better maintainability and organization.
"""
import streamlit as st

# Import UI modules
from src.ui.job_analyzer import render_job_analyzer, get_keywords_for_rewrite
from src.ui.resume_optimizer import render_resume_optimizer, render_example_section
from src.ui.file_management import render_saved_files_section
from src.app_utils import initialize_app, initialize_all_session_state


def main():
    """Main application entry point"""
    # Initialize the app
    initialize_app()

    # Initialize all session state variables
    initialize_all_session_state()

    # Render main sections
    render_job_analyzer()

    # Get keywords for rewrite if available
    keywords_for_rewrite = get_keywords_for_rewrite()

    # Only show these sections if not using streamlined workflow
    if keywords_for_rewrite or st.session_state.get('analyzed_keywords'):
        st.markdown("---")
        st.markdown("### 🔧 Resume Optimization (Advanced)")
        render_resume_optimizer(keywords_for_rewrite)

    # Example section
    # render_example_section()

    # Saved files management
    st.markdown("---")
    render_saved_files_section()


if __name__ == "__main__":
    main()

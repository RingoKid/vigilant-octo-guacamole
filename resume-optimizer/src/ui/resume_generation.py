"""
Resume generation UI components
"""
import streamlit as st
from src.resume_generator import ResumeGenerator


def render_resume_generation_section():
    """Render the resume generation section"""
    if 'last_optimization_result' in st.session_state and st.session_state['last_optimization_result']:
        st.header("📄 Resume Generation")

        if st.button("🔄 Generate Updated Resume"):
            _generate_updated_resume()


def _generate_updated_resume():
    """Generate updated resume from optimization result"""
    with st.spinner("Generating updated resume..."):
        try:
            resume_generator = ResumeGenerator()

            # Generate updated resume
            resume_generator.generate_updated_resume(
                st.session_state['last_optimization_result'])

            st.success("✅ Updated resume generated successfully!")

        except Exception as e:
            st.error(f"Error generating resume: {e}")

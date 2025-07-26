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

        # Show resume content if resume has been generated
        if 'updated_resume_html' in st.session_state and st.session_state['updated_resume_html']:
            _render_updated_resume()


def _generate_updated_resume():
    """Generate updated resume from optimization result"""
    with st.spinner("Generating updated resume..."):
        try:
            resume_generator = ResumeGenerator()

            # Read original resume
            with open("/workspaces/agents/resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
                original_resume = file.read()

            # Generate updated resume (HTML)
            updated_resume_html = resume_generator.generate_updated_resume(
                st.session_state['last_optimization_result'])

            # Generate markdown version for display
            updated_resume_markdown = resume_generator.generate_markdown_from_html(
                updated_resume_html)

            # Store for later use
            st.session_state['updated_resume_html'] = updated_resume_html
            st.session_state['updated_resume_markdown'] = updated_resume_markdown

            st.success("✅ Updated resume generated successfully!")

        except Exception as e:
            st.error(f"Error generating resume: {e}")


def _render_updated_resume():
    """Render the updated resume content"""
    st.subheader("Updated Resume Content")

    # Display HTML content
    st.markdown("**HTML Preview:**")
    st.code(st.session_state['updated_resume_html'], language='html')

    st.markdown("**Rendered Preview:**")
    st.markdown(st.session_state['updated_resume_markdown'])

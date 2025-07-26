"""
Resume generation and PDF creation UI components
"""
import streamlit as st
import difflib
import os
from src.resume_generator import ResumeGenerator, save_resume_html, save_resume_markdown


def render_resume_generation_section():
    """Render the resume generation and PDF creation section"""
    if 'last_optimization_result' in st.session_state and st.session_state['last_optimization_result']:
        st.header("📄 Resume Generation & PDF Creation")

        if st.button("🔄 Generate Updated Resume"):
            _generate_updated_resume()

        # Show diff and PDF options if resume has been generated
        if 'updated_resume_html' in st.session_state and st.session_state['updated_resume_html']:
            _render_resume_tabs()


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

            # Generate markdown version for diff viewing
            updated_resume_markdown = resume_generator.generate_markdown_from_html(
                updated_resume_html)

            # Store for later use
            st.session_state['original_resume'] = original_resume
            st.session_state['updated_resume_html'] = updated_resume_html
            st.session_state['updated_resume_markdown'] = updated_resume_markdown

            st.success("✅ Updated resume generated successfully!")

        except Exception as e:
            st.error(f"Error generating resume: {e}")


def _render_resume_tabs():
    """Render tabs for different resume views"""
    tab1, tab2, tab3 = st.tabs(
        ["📋 Updated Resume", "🔍 View Differences", "📄 Create PDF"])

    with tab1:
        _render_updated_resume_tab()

    with tab2:
        _render_differences_tab()

    with tab3:
        _render_pdf_creation_tab()


def _render_updated_resume_tab():
    """Render the updated resume tab"""
    st.subheader("Updated Resume Content")

    # Display HTML content
    st.markdown("**HTML Preview:**")
    st.code(st.session_state['updated_resume_html'], language='html')

    st.markdown("**Rendered Preview:**")
    st.markdown(st.session_state['updated_resume_markdown'])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save as HTML", key="save_html"):
            _save_resume_html()

    with col2:
        if st.button("💾 Save as Markdown", key="save_md"):
            _save_resume_markdown()


def _render_differences_tab():
    """Render the differences tab"""
    st.subheader("Resume Differences")
    st.info("Compare the original resume with the updated version. Green indicates additions, red indicates removals.")

    try:
        original_lines = st.session_state['original_resume'].splitlines()
        updated_lines = st.session_state['updated_resume_markdown'].splitlines(
        )

        # Create a simple diff display
        diff = list(difflib.unified_diff(
            original_lines, updated_lines,
            fromfile='Original Resume', tofile='Updated Resume',
            lineterm='', n=3
        ))

        if diff:
            _display_diff(diff)
        else:
            st.info("No differences found between original and updated resume.")

        # Side-by-side comparison
        _display_side_by_side_comparison()

    except Exception as e:
        st.error(f"Error generating diff: {e}")


def _render_pdf_creation_tab():
    """Render the PDF creation tab"""
    st.subheader("PDF Generation")
    st.info("Create a professional PDF version of your updated resume.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("**PDF Preview Options:**")
        st.write("• Professional formatting")
        st.write("• ATS-friendly layout")
        st.write("• Clean typography")
        st.write("• Optimized for printing")

    with col2:
        if st.button("📄 Create PDF", key="create_pdf"):
            _create_pdf()


def _save_resume_html():
    """Save resume as HTML"""
    try:
        saved_path = save_resume_html(st.session_state['updated_resume_html'])
        st.success(f"✅ Resume saved to: {saved_path.split('/')[-1]}")
    except Exception as e:
        st.error(f"Error saving resume: {e}")


def _save_resume_markdown():
    """Save resume as Markdown"""
    try:
        saved_path = save_resume_markdown(
            st.session_state['updated_resume_markdown'])
        st.success(f"✅ Resume saved to: {saved_path.split('/')[-1]}")
    except Exception as e:
        st.error(f"Error saving resume: {e}")


def _display_diff(diff):
    """Display diff in a readable format"""
    diff_text = ""
    for line in diff:
        if line.startswith('+++') or line.startswith('---'):
            continue
        elif line.startswith('@@'):
            diff_text += f"\n**{line}**\n"
        elif line.startswith('+') and not line.startswith('+++'):
            diff_text += f"🟢 **Added:** {line[1:]}\n"
        elif line.startswith('-') and not line.startswith('---'):
            diff_text += f"🔴 **Removed:** {line[1:]}\n"
        else:
            diff_text += f"   {line}\n"

    st.markdown(diff_text)


def _display_side_by_side_comparison():
    """Display side-by-side comparison"""
    st.subheader("Side-by-Side Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Original Resume**")
        st.text_area("", value=st.session_state['original_resume'],
                     height=400, key="original_display")

    with col2:
        st.write("**Updated Resume**")
        st.text_area("", value=st.session_state['updated_resume_markdown'],
                     height=400, key="updated_display")


def _create_pdf():
    """Create PDF from updated resume"""
    with st.spinner("Creating PDF..."):
        try:
            resume_generator = ResumeGenerator()
            pdf_path = resume_generator.create_pdf(
                st.session_state['updated_resume_html'])

            # Provide download link
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()

            st.success("✅ PDF created successfully!")
            st.download_button(
                label="📥 Download PDF",
                data=pdf_data,
                file_name=f"resume_{os.path.basename(pdf_path)}",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Error creating PDF: {e}")

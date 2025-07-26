"""
File management UI components
"""
import streamlit as st
from src.file_manager import list_saved_files, load_saved_file
from src.resume_generator import ResumeGenerator


def render_saved_files_section():
    """Render the saved files management section"""
    st.header("📁 Saved Files Management")
    st.info("View and manage previously generated files from both chains.")

    # Create tabs for different file types
    tab1, tab2 = st.tabs(
        ["📊 Job Analysis Files", "📝 Resume Optimization Files"])

    with tab1:
        _render_job_analysis_files()

    with tab2:
        _render_resume_optimization_files()

    _render_summary_statistics()


def _render_job_analysis_files():
    """Render job analysis files section"""
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
                        _show_job_analysis_details(filename)
        else:
            st.info(
                "No job analysis files found. Analyze a job description to create your first file!")
    except Exception as e:
        st.error(f"Error listing job analysis files: {e}")


def _render_resume_optimization_files():
    """Render resume optimization files section"""
    st.subheader("Resume Optimization Results")
    try:
        saved_files = list_saved_files("resume_optimization")
        resume_opt_files = saved_files.get("resume_optimization", [])

        if resume_opt_files:
            st.write(
                f"Found {len(resume_opt_files)} saved resume optimization files:")
            for i, filename in enumerate(sorted(resume_opt_files, reverse=True)):
                with st.expander(f"📄 {filename}", expanded=False):
                    _render_optimization_file_actions(filename, i)

            # Add bulk PDF generation option
            _render_bulk_pdf_generation(resume_opt_files)
        else:
            st.info(
                "No resume optimization files found. Run a resume optimization to create your first file!")
    except Exception as e:
        st.error(f"Error listing resume optimization files: {e}")


def _show_job_analysis_details(filename):
    """Show details for a job analysis file"""
    try:
        file_data = load_saved_file("job_analysis", filename)

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Metadata:**")
            st.json(file_data["metadata"])
        with col2:
            st.write("**Input Preview:**")
            st.write(file_data["input"]["job_description_preview"])

        st.write("**Analysis Result:**")
        st.json(file_data["output"]["analysis_result"])
    except Exception as e:
        st.error(f"Error loading file: {e}")


def _render_optimization_file_actions(filename, index):
    """Render actions for optimization files"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button(f"Show Details", key=f"resume_opt_{index}"):
            _show_optimization_details(filename)

    with col2:
        if st.button(f"📄 Generate PDF", key=f"generate_pdf_{index}"):
            _generate_pdf_from_file(filename)

    with col3:
        if st.button(f"🔄 Load & Use", key=f"load_use_{index}"):
            _load_and_use_optimization(filename)


def _show_optimization_details(filename):
    """Show details for an optimization file"""
    try:
        file_data = load_saved_file("resume_optimization", filename)

        col1_details, col2_details = st.columns(2)
        with col1_details:
            st.write("**Metadata:**")
            st.json(file_data["metadata"])
            st.write("**Keywords Used:**")
            st.write(", ".join(file_data["input"]["keywords_used"]))
        with col2_details:
            st.write("**Keywords Source:**")
            st.write(file_data["metadata"]["keywords_source"])
            st.write("**Keywords Count:**")
            st.write(file_data["input"]["keywords_count"])

        st.write("**Optimization Result:**")
        result = file_data["output"]["optimization_result"]
        if isinstance(result, dict):
            st.write("**Updated Summary:**")
            st.write(result.get('updated_summary', 'N/A'))

            for section in ['liberty_mutual_group', 'inovace_technologies',
                            'spider_digital_commerce', 'echo_project']:
                if section in result and result[section]:
                    st.write(f"**{section.replace('_', ' ').title()}:**")
                    for bullet in result[section]:
                        st.write(f"• {bullet}")
        else:
            st.json(result)
    except Exception as e:
        st.error(f"Error loading file: {e}")


def _generate_pdf_from_file(filename):
    """Generate PDF from saved optimization file"""
    try:
        file_data = load_saved_file("resume_optimization", filename)
        optimization_result = file_data["output"]["optimization_result"]

        with st.spinner("Generating PDF from saved optimization..."):
            # Generate HTML resume
            resume_generator = ResumeGenerator()
            updated_resume_html = resume_generator.generate_updated_resume(
                optimization_result)

            # Create PDF
            pdf_path = resume_generator.create_pdf(updated_resume_html)

            # Provide download link
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()

            st.success(f"✅ PDF generated from {filename}!")
            st.download_button(
                label="📥 Download PDF",
                data=pdf_data,
                file_name=f"resume_from_{filename.replace('.json', '.pdf')}",
                mime="application/pdf",
                key=f"download_pdf_{filename}"
            )

    except Exception as e:
        st.error(f"Error generating PDF: {e}")


def _load_and_use_optimization(filename):
    """Load optimization result into current session"""
    try:
        file_data = load_saved_file("resume_optimization", filename)
        optimization_result = file_data["output"]["optimization_result"]

        # Load this optimization result into the current session
        st.session_state['last_optimization_result'] = optimization_result
        st.success(f"✅ Loaded optimization from {filename}!")
        st.info("You can now use the 'Resume Generation & PDF Creation' section above to work with this optimization.")

    except Exception as e:
        st.error(f"Error loading optimization: {e}")


def _render_bulk_pdf_generation(resume_opt_files):
    """Render bulk PDF generation section"""
    st.subheader("🚀 Bulk PDF Generation")
    st.info("Generate PDFs from multiple optimization files at once.")

    if st.button("📄 Generate PDFs from All Optimization Files"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        success_count = 0

        for i, filename in enumerate(resume_opt_files):
            try:
                status_text.text(f"Processing {filename}...")
                progress_bar.progress((i + 1) / len(resume_opt_files))

                file_data = load_saved_file("resume_optimization", filename)
                optimization_result = file_data["output"]["optimization_result"]

                # Generate HTML resume and PDF
                resume_generator = ResumeGenerator()
                updated_resume_html = resume_generator.generate_updated_resume(
                    optimization_result)
                pdf_path = resume_generator.create_pdf(updated_resume_html)

                success_count += 1

            except Exception as e:
                st.error(f"Error processing {filename}: {e}")

        status_text.text("Bulk PDF generation complete!")
        st.success(
            f"✅ Successfully generated {success_count} PDFs from {len(resume_opt_files)} optimization files!")
        st.info("Check the outputs folder for all generated PDFs.")


def _render_summary_statistics():
    """Render summary statistics"""
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

"""
Job Description Analyzer UI components
"""
import streamlit as st
from src.chains import get_analyzer_chain, get_rewriter_chain
from src.file_manager import save_job_analysis_result, save_resume_optimization_result
from src.resume_generator import ResumeGenerator


def render_job_analyzer():
    """Render the job description analyzer section"""
    st.header("🔍 Job Description Analyzer")

    job_description = st.text_area(
        "Paste a job description to analyze:", height=200)

    # Streamlined single-button workflow
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Analyze & Optimize Resume (All-in-One)", type="primary"):
            if job_description:
                _streamlined_workflow(job_description)
            else:
                st.warning("Please paste a job description first.")

    with col2:
        if st.button("📊 Analyze Job Description Only"):
            if job_description:
                _analyze_job_description(job_description)
            else:
                st.warning("Please paste a job description first.")

    _render_keywords_usage_section()


def _streamlined_workflow(job_description):
    """Complete streamlined workflow: analyze job description, optimize resume, and generate PDF"""
    try:
        # Step 1: Analyze job description
        with st.spinner("Step 1/4: Analyzing job description..."):
            analyzer_chain = get_analyzer_chain()
            analysis_result = analyzer_chain.invoke(
                {"job_description": job_description})
            st.session_state['analyzed_keywords'] = analysis_result

            # Save the analysis result
            try:
                saved_analysis_path = save_job_analysis_result(
                    job_description, analysis_result)
                st.success(
                    f"✅ Job analysis saved to: {saved_analysis_path.split('/')[-1]}")
            except Exception as e:
                st.warning(f"Analysis completed but couldn't save file: {e}")

        # Step 2: Extract keywords for rewrite
        with st.spinner("Step 2/4: Extracting keywords..."):
            keywords = []
            for key in ['technical_skills', 'technologies_and_tools', 'soft_skills']:
                keywords += analysis_result.get(key, [])
            st.session_state['keywords_for_rewrite'] = keywords

            st.info(
                f"📋 Extracted {len(keywords)} keywords from job description")

        # Step 3: Optimize resume with keywords
        with st.spinner("Step 3/4: Optimizing resume with extracted keywords..."):
            rewriter_chain = get_rewriter_chain()
            with open("resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
                resume_text = file.read()

            optimization_result = rewriter_chain.invoke({
                "keywords_to_integrate": keywords,
                "original_resume_text": resume_text
            })

            st.session_state['last_optimization_result'] = optimization_result

            # Save the optimization result
            try:
                saved_optimization_path = save_resume_optimization_result(
                    keywords, resume_text, optimization_result, "streamlined_workflow"
                )
                st.success(
                    f"✅ Resume optimization saved to: {saved_optimization_path.split('/')[-1]}")
            except Exception as e:
                st.warning(
                    f"Optimization completed but couldn't save file: {e}")

        # Step 4: Generate updated resume PDF
        with st.spinner("Step 4/4: Generating updated resume PDF..."):
            resume_generator = ResumeGenerator()
            updated_resume_html = resume_generator.generate_updated_resume(
                optimization_result)
            pdf_path = resume_generator.create_pdf(updated_resume_html)

            # Store PDF path for download
            st.session_state['streamlined_pdf_path'] = pdf_path
            st.success(f"✅ PDF generated: {pdf_path.split('/')[-1]}")

        # Display results
        st.success(
            "🎉 **Complete! Your resume has been optimized and PDF generated.**")

        # Show download button
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()

            st.download_button(
                label="📥 Download Optimized Resume PDF",
                data=pdf_data,
                file_name=f"optimized_resume_streamlined.pdf",
                mime="application/pdf",
                key="download_streamlined_pdf"
            )
        except Exception as e:
            st.error(f"Error preparing PDF download: {e}")

        # Show summary of what was done
        with st.expander("📊 View Optimization Summary"):
            st.subheader("Job Analysis Results")
            st.json(analysis_result)

            st.subheader("Keywords Used for Optimization")
            st.write(", ".join(keywords))

            st.subheader("Optimized Resume Content")
            st.json(optimization_result)

    except Exception as e:
        st.error(f"❌ Error in streamlined workflow: {e}")
        st.error(
            "Please try using the individual steps if the streamlined process fails.")


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

"""
Resume optimization UI components
"""
import streamlit as st
from src.chains import get_rewriter_chain
from src.file_manager import save_resume_optimization_result
from src.parsers import JobDescriptionKeywords
from src.resume_generator import ResumeGenerator


def render_resume_optimizer(keywords_for_rewrite):
    """Render the resume optimization section"""
    if keywords_for_rewrite:
        if st.button("🚀 Generate Optimized Resume & PDF"):
            _process_resume_with_keywords(keywords_for_rewrite, "job_analysis")

    # Show download button if PDF is available
    if 'generated_pdf_path' in st.session_state and st.session_state['generated_pdf_path']:
        st.success("✅ Resume and PDF generated successfully!")

        try:
            with open(st.session_state['generated_pdf_path'], "rb") as pdf_file:
                pdf_data = pdf_file.read()

            st.download_button(
                label="📥 Download Resume PDF",
                data=pdf_data,
                file_name=f"optimized_resume.pdf",
                mime="application/pdf",
                key="download_optimized_pdf"
            )
        except Exception as e:
            st.error(f"Error preparing PDF download: {e}")


def render_example_section():
    """Render the example usage section"""
    st.header("🧑‍💻 Example: Resume Rewriter with Example Keywords")
    st.info("Use the example resume and keywords to see how the rewriter chain works.")

    if st.button("🚀 Run Resume Rewriter Example & Generate PDF"):
        _run_example_optimization()

    # Show download button if PDF is available from example
    if 'example_pdf_path' in st.session_state and st.session_state['example_pdf_path']:
        st.success("✅ Example resume and PDF generated successfully!")

        try:
            with open(st.session_state['example_pdf_path'], "rb") as pdf_file:
                pdf_data = pdf_file.read()

            st.download_button(
                label="📥 Download Example Resume PDF",
                data=pdf_data,
                file_name=f"example_resume.pdf",
                mime="application/pdf",
                key="download_example_pdf"
            )
        except Exception as e:
            st.error(f"Error preparing example PDF download: {e}")


def _process_resume_with_keywords(keywords_list, source_type):
    """Process resume with given keywords and generate PDF"""
    with st.spinner("Generating optimized resume and PDF..."):
        try:
            # Step 1: Generate optimized resume content
            rewriter_chain = get_rewriter_chain()
            with open("resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
                resume_text = file.read()

            result = rewriter_chain.invoke({
                "keywords_to_integrate": keywords_list,
                "original_resume_text": resume_text
            })

            st.subheader("🎯 Keywords Used")
            st.write(", ".join(keywords_list))
            st.subheader("📝 Optimized Resume Content")
            st.json(result)

            # Store the result for resume generation
            st.session_state['last_optimization_result'] = result

            # Step 2: Generate HTML and PDF
            resume_generator = ResumeGenerator()
            updated_resume_html = resume_generator.generate_updated_resume(
                result)
            pdf_path = resume_generator.create_pdf(updated_resume_html)

            # Store PDF path for download
            st.session_state['generated_pdf_path'] = pdf_path

            # Save the optimization result
            try:
                saved_file_path = save_resume_optimization_result(
                    keywords_list, resume_text, result, source_type
                )
                st.success(
                    f"✅ Optimization and PDF saved! JSON: {saved_file_path.split('/')[-1]}")
                st.success(f"✅ PDF saved to: {pdf_path.split('/')[-1]}")
            except Exception as e:
                st.warning(
                    f"Optimization completed but couldn't save file: {e}")

        except Exception as e:
            st.error(f"Error processing resume: {e}")


def _run_example_optimization():
    """Run the example optimization with predefined keywords and generate PDF"""
    with st.spinner("Generating example resume and PDF..."):
        try:
            # Step 1: Generate optimized resume content
            rewriter_chain = get_rewriter_chain()
            with open("resume-optimizer/src/docs/resume.md", "r", encoding="utf-8") as file:
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

            _display_example_results(job_keywords, result)

            # Store the result for resume generation
            st.session_state['last_optimization_result'] = result

            # Step 2: Generate HTML and PDF
            resume_generator = ResumeGenerator()
            updated_resume_html = resume_generator.generate_updated_resume(
                result)
            pdf_path = resume_generator.create_pdf(updated_resume_html)

            # Store PDF path for download
            st.session_state['example_pdf_path'] = pdf_path

            # Save the optimization result
            try:
                saved_file_path = save_resume_optimization_result(
                    all_keywords, resume_text, result, "example"
                )
                st.success(
                    f"✅ Example optimization and PDF saved! JSON: {saved_file_path.split('/')[-1]}")
                st.success(f"✅ PDF saved to: {pdf_path.split('/')[-1]}")
            except Exception as e:
                st.warning(f"Example completed but couldn't save file: {e}")

        except Exception as e:
            st.error(f"Error processing resume: {e}")


def _display_example_results(job_keywords, result):
    """Display example optimization results"""
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

    for section_key, section_name in [
        ('liberty_mutual_group', 'Liberty Mutual Group Experience'),
        ('inovace_technologies', 'Inovace Technologies Experience'),
        ('spider_digital_commerce', 'Spider Digital Commerce Experience'),
        ('echo_project', 'Echo Project Experience')
    ]:
        st.write(f"**{section_name}:**")
        for bullet in result[section_key]:
            st.write(f"• {bullet}")

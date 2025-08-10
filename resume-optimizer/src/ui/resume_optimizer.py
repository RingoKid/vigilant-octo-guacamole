"""
Resume optimization UI components
"""
import streamlit as st
from src.chains import get_rewriter_chain
from src.file_manager import save_resume_optimization_result
from src.parsers import JobDescriptionKeywords


def render_resume_optimizer(keywords_for_rewrite):
    """Render the resume optimization section"""
    if keywords_for_rewrite:
        if st.button("Rewrite Resume with Analyzed Keywords"):
            _process_resume_with_keywords(keywords_for_rewrite, "job_analysis")


def render_custom_keywords_section():
    """Render the custom keywords section"""
    st.subheader("🔧 Custom Keywords")
    custom_keywords = st.text_area(
        "Enter custom keywords (comma-separated):",
        value="Python, AWS, Docker, Kubernetes, CI/CD, REST APIs, Machine Learning",
        height=100
    )

    if st.button("Rewrite with Custom Keywords"):
        if custom_keywords:
            keywords_list = [kw.strip()
                             for kw in custom_keywords.split(",") if kw.strip()]
            _process_resume_with_keywords(keywords_list, "custom")
        else:
            st.warning("Please enter some keywords first.")


def render_example_section():
    """Render the example usage section"""
    st.header("🧑‍💻 Example: Resume Rewriter with Example Keywords")
    st.info("Use the example resume and keywords to see how the rewriter chain works.")

    if st.button("Run Resume Rewriter Example"):
        _run_example_optimization()


def _process_resume_with_keywords(keywords_list, source_type):
    """Process resume with given keywords"""
    with st.spinner("Processing resume with keywords..."):
        try:
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

            # Save the optimization result
            try:
                saved_file_path = save_resume_optimization_result(
                    keywords_list, resume_text, result, source_type
                )
                st.success(
                    f"✅ Optimization saved to: {saved_file_path.split('/')[-1]}")
            except Exception as e:
                st.warning(
                    f"Optimization completed but couldn't save file: {e}")

        except Exception as e:
            st.error(f"Error processing resume: {e}")


def _run_example_optimization():
    """Run the example optimization with predefined keywords"""
    with st.spinner("Processing resume with example keywords..."):
        try:
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

            # Save the optimization result
            try:
                saved_file_path = save_resume_optimization_result(
                    all_keywords, resume_text, result, "example"
                )
                st.success(
                    f"✅ Example optimization saved to: {saved_file_path.split('/')[-1]}")
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

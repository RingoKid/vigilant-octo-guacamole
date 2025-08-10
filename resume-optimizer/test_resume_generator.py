# Test Resume Generator

from src.resume_generator import ResumeGenerator
import json

# Test data (example optimization result)
test_optimization_result = {
    "updated_summary": "Software Developer with 4+ years in backend development, specializing in Java (Spring Boot) microservices and distributed systems architecture. Proven experience in end-to-end software development, building and scaling enterprise applications for 500,000+ users in high-volume production environments.",
    "liberty_mutual_group": [
        "Enhanced reliability of a Java-based distributed systems architecture by diagnosing and resolving 200+ production issues in Spring Boot microservices, reducing incident response time by 40% through meticulous log analysis.",
        "Performed root-cause analysis on recurring production issues, refactoring critical Java code using Object-Oriented Design principles and creating system documentation to prevent future incidents and ensure system stability.",
        "Optimized report-generation algorithms and memory management, scaling system capacity to support 3x larger datasets and raising the Excel file-size limit to 100MB for high-volume production environments."
    ],
    "inovace_technologies": [
        "Drove end-to-end development for a new HRM software platform, integrating 3 IoT device types and serving 500,000+ employees across 1,200+ organizations using Java (Spring Boot) and MySQL.",
        "Collaborated in a cross-functional team to integrate Flutter (Android/iOS), Laravel, and Java microservices, ensuring architectural alignment across the backend development stack for seamless product delivery.",
        "Improved system scalability by reducing API response time by 60% through strategic caching with Redis and database query optimization in MySQL and PostgreSQL, enhancing the user experience for 500k+ employees."
    ],
    "spider_digital_commerce": [
        "Independently architected and executed the end-to-end development of a native Android app using Java and Firebase, successfully launching a system that processed 1,000+ daily transactions for 5,000+ active users."
    ],
    "echo_project": [
        "Engineered a full-stack donation platform using Python, Django, and PostgreSQL, applying Object-Oriented Design patterns to build a secure system processing ~$1M in annual donations.",
        "Implemented robust user Identity Access Management with secure authentication and integrated payment gateways and automation for email notifications, ensuring a streamlined and secure donor experience."
    ]
}


def test_resume_generation():
    print("Testing Resume Generator...")

    # Initialize generator
    generator = ResumeGenerator()

    # Generate updated resume
    updated_resume = generator.generate_updated_resume(
        test_optimization_result)

    print("✅ Updated resume generated successfully!")
    print("\n" + "="*50)
    print("GENERATED RESUME:")
    print("="*50)
    print(updated_resume[:500] + "...")

    # Test PDF creation
    try:
        pdf_path = generator.create_pdf(updated_resume)
        print(f"\n✅ PDF created successfully at: {pdf_path}")
    except Exception as e:
        print(f"❌ PDF creation failed: {e}")

    # Test diff generation
    try:
        with open("resume-optimizer/src/docs/resume.md", "r") as f:
            original_resume = f.read()

        diff_html = generator.get_diff_html(original_resume, updated_resume)
        print("✅ Diff HTML generated successfully!")
        print(f"Diff HTML length: {len(diff_html)} characters")
    except Exception as e:
        print(f"❌ Diff generation failed: {e}")


if __name__ == "__main__":
    test_resume_generation()

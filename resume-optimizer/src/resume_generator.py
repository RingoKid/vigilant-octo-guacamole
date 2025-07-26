# resume_generator.py

import os
import difflib
from datetime import datetime
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import re
from string import Template


class ResumeGenerator:
    def __init__(self):
        self.template_path = self._get_template_path()

    def _get_template_path(self):
        """Get the path to the HTML template"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, 'templates', 'resume_template.html')

    def _load_template(self):
        """Load the HTML template"""
        with open(self.template_path, 'r', encoding='utf-8') as file:
            return file.read()

    def generate_updated_resume(self, optimization_result, original_resume_path=None):
        """Generate updated resume HTML from optimization result"""
        if original_resume_path is None:
            original_resume_path = "/workspaces/agents/resume-optimizer/src/docs/resume.md"

        # Read original resume to extract static data
        with open(original_resume_path, 'r', encoding='utf-8') as file:
            original_content = file.read()

        # Extract static information from original resume
        static_info = self._extract_static_info(original_content)

        # Format bullets for each section
        liberty_bullets = self._format_bullets_html(
            optimization_result.get('liberty_mutual_group', []))
        inovace_bullets = self._format_bullets_html(
            optimization_result.get('inovace_technologies', []))
        spider_bullets = self._format_bullets_html(
            optimization_result.get('spider_digital_commerce', []))
        echo_bullets = self._format_bullets_html(
            optimization_result.get('echo_project', []))

        # Load template
        template_html = self._load_template()

        # Fill template with data using Template (safer for HTML with CSS)
        template = Template(template_html)
        updated_resume = template.substitute(
            NAME=static_info['name'],
            EMAIL=static_info['email'],
            PHONE=static_info['phone'],
            LOCATION=static_info['location'],
            LINKEDIN_URL=static_info['linkedin_url'],
            GITHUB_URL=static_info['github_url'],
            SUMMARY_TEXT=optimization_result.get(
                'updated_summary', static_info['summary']),

            # Liberty Mutual
            LIBERTY_MUTUAL_DATES=static_info['liberty_mutual_dates'],
            LIBERTY_MUTUAL_LOCATION=static_info['liberty_mutual_location'],
            LIBERTY_MUTUAL_BULLETS=liberty_bullets,
            LIBERTY_MUTUAL_TECH_STACK=static_info['liberty_mutual_tech_stack'],

            # Inovace Technologies
            INOVACE_DATES=static_info['inovace_dates'],
            INOVACE_LOCATION=static_info['inovace_location'],
            INOVACE_BULLETS=inovace_bullets,
            INOVACE_TECH_STACK=static_info['inovace_tech_stack'],

            # Spider Digital Commerce
            SPIDER_DATES=static_info['spider_dates'],
            SPIDER_LOCATION=static_info['spider_location'],
            SPIDER_BULLETS=spider_bullets,
            SPIDER_TECH_STACK=static_info['spider_tech_stack'],

            # Echo Project
            ECHO_BULLETS=echo_bullets,

            # Education
            GSU_DATES=static_info['gsu_dates'],
            GSU_LOCATION=static_info['gsu_location'],
            NSU_DATES=static_info['nsu_dates'],
            NSU_LOCATION=static_info['nsu_location'],

            # Skills
            SKILLS_LANGUAGES=static_info['skills_languages'],
            SKILLS_FRAMEWORKS=static_info['skills_frameworks'],
            SKILLS_DATABASES=static_info['skills_databases']
        )

        return updated_resume

    def _extract_static_info(self, original_content):
        """Extract static information from original resume"""
        lines = original_content.split('\n')

        info = {
            'name': 'Naimul Islam',
            'email': 'rifat.naimul@gmail.com',
            'phone': '(669) 273-5676',
            'location': 'Atlanta, GA',
            'linkedin_url': '#',
            'github_url': '#',
            'summary': 'Software Developer with 4 years of experience...',

            # Job details
            'liberty_mutual_dates': 'Oct 2022 – Dec 2024',
            'liberty_mutual_location': 'Bangkok, Thailand',
            'liberty_mutual_tech_stack': 'Java, Spring Boot, Angular, Asp.Net, Jenkins, MSSQL, PostgreSQL',

            'inovace_dates': 'Feb 2020 – Aug 2022',
            'inovace_location': 'Dhaka, Bangladesh',
            'inovace_tech_stack': 'Flutter, Laravel, Spring Boot, MySQL, PostgreSQL, Redis, Vue.js, AngularJs',

            'spider_dates': 'Jun 2019 – Aug 2019',
            'spider_location': 'Dhaka, Bangladesh',
            'spider_tech_stack': 'Android, Java, Firebase, RESTful APIs',

            # Education
            'gsu_dates': 'Expected Dec 2025',
            'gsu_location': 'Atlanta, GA',
            'nsu_dates': '2015-2019',
            'nsu_location': 'Dhaka, Bangladesh',

            # Skills
            'skills_languages': 'C/C++, Java, Python, JavaScript, PHP, Dart, Bash',
            'skills_frameworks': 'Spring Boot, Django, Flask, Angular, Vue.js, Flutter, Docker, Jenkins, Git, Linux, CI/CD, RESTful APIs, Android Studio, Firebase, Postman, ASP.NET, JUnit, Mockito, AWS',
            'skills_databases': 'MySQL, PostgreSQL, Oracle, MSSQL, Redis, MongoDB'
        }

        # Extract actual data from content
        for i, line in enumerate(lines):
            if line.startswith('# ') and len(line.strip()) > 2:
                info['name'] = line[2:].strip()
            elif '❖' in line and '@' in line:
                # Parse contact line: email ❖ phone ❖ location ❖ LinkedIn ❖ GitHub
                contact_line = line.strip().lstrip('##').strip()
                parts = [part.strip() for part in contact_line.split('❖')]
                if len(parts) >= 3:
                    info['email'] = parts[0].strip()
                    info['phone'] = parts[1].strip()
                    info['location'] = parts[2].strip()
            elif line.strip().startswith('**Software Developer') and 'experience' in line:
                # Extract summary paragraph
                summary_lines = []
                for j in range(i, min(i+10, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('WORK EXPERIENCE'):
                        summary_lines.append(lines[j].strip())
                    elif lines[j].startswith('WORK EXPERIENCE'):
                        break
                info['summary'] = ' '.join(summary_lines)
                break

        return info

    def _format_bullets_html(self, bullets_list):
        """Format bullet points for HTML"""
        if not bullets_list:
            return ""

        formatted = []
        for bullet in bullets_list:
            formatted.append(f"<li>{bullet}</li>")

        return '\n'.join(formatted)

    def get_diff_html(self, original_resume, updated_resume):
        """Generate HTML diff between original and updated resume"""
        original_lines = original_resume.splitlines(keepends=True)
        updated_lines = updated_resume.splitlines(keepends=True)

        # Convert diff to HTML
        html_diff = difflib.HtmlDiff()
        diff_html = html_diff.make_file(
            original_lines,
            updated_lines,
            fromdesc='Original Resume',
            todesc='Updated Resume',
            context=True,
            numlines=3
        )

        return diff_html

    def create_pdf(self, resume_html, output_path=None):
        """Create PDF from HTML resume using WeasyPrint"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/workspaces/agents/resume-optimizer/outputs/resume_pdf_{timestamp}.pdf"

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Create PDF from HTML
        font_config = FontConfiguration()
        html_doc = HTML(string=resume_html)

        # Additional CSS for PDF optimization
        pdf_css = CSS(string='''
            @page {
                size: A4;
                margin: 1in;
            }
            body {
                font-size: 11pt;
                line-height: 1.4;
            }
            .container {
                max-width: none;
                padding: 0;
            }
        ''')

        html_doc.write_pdf(output_path, stylesheets=[
                           pdf_css], font_config=font_config)

        return output_path

    def generate_markdown_from_html(self, html_content):
        """Convert HTML back to markdown for display purposes"""
        # This is a simplified conversion - mainly for the diff viewer
        # Remove HTML tags and convert to basic markdown
        import re

        # Remove HTML tags but keep content
        markdown_content = re.sub(r'<[^>]+>', '', html_content)

        # Clean up extra whitespace
        markdown_content = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown_content)

        return markdown_content.strip()


def save_resume_html(resume_content, filename=None):
    """Save resume HTML to file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"updated_resume_{timestamp}.html"

    output_dir = "/workspaces/agents/resume-optimizer/outputs/resumes"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(resume_content)

    return filepath


def save_resume_markdown(resume_content, filename=None):
    """Save resume markdown to file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"updated_resume_{timestamp}.md"

    output_dir = "/workspaces/agents/resume-optimizer/outputs/resumes"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(resume_content)

    return filepath

# prompts.py
# Central location for all prompt templates used by AIEngine and related services.

KEYWORD_EXTRACTION_PROMPT = """
You are an expert at analyzing job descriptions. Your task is to identify the most important keywords from the text provided.
These keywords should represent the core skills, technologies, and responsibilities.

Please return the keywords as a single, comma-separated string.

Job Description:
{text}

Keywords:
"""

# Add more prompts here as needed, e.g.:
# SUMMARY_PROMPT = "..."

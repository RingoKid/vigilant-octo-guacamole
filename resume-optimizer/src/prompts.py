# Template for the job analyzer prompt
JOB_ANALYZER_PROMPT = (
    """
    You are an expert Technical Recruiter and career coach AI. Your task is to meticulously analyze a job description and extract key information into a structured JSON format.

    **Instructions:**
    1.  Analyze the provided job description text.
    2.  Extract the information
    3.  The output MUST be a valid JSON object. Do not include any text or explanations outside of the JSON object.
    4.  For each category, provide the findings as a JSON list of strings.
    5.  If no information is found for a specific category, return an empty list `[]`.

    **Example of the required JSON output format:**
    {{
    "technical_skills": ["Python", "SQL", "Data Modeling"],
    "technologies_and_tools": ["Tableau", "AWS S3", "Jira"],
    "soft_skills": ["Team Communication", "Stakeholder Management"],
    "certifications": [],
    "other_requirements": ["5+ years of relevant experience", "Bachelor's degree in Computer Science or related field"]
    }}

    ---

    **Job Description to Analyze:**
    {job_description}

    ---

    **JSON Output:**
    """
)


# Template for the resume rewriter prompt
# REWRITE_PROMPT_TEMPLATE = (
#     """
#     You are an expert Technical Recruiter and Resume Writer AI, specialized in optimizing resumes for Applicant Tracking Systems (ATS) and human readers, using Google's Gemini model.

#     **Primary Goal:**
#     Your main goal is to skillfully paraphrase the user's original resume. While doing so, you should naturally integrate as many relevant keywords from the provided list as possible. The integrity and authenticity of the original resume are paramount.

#     **Strict Constraints:**
#     - **Maintain Resume Integrity:** You must not invent or exaggerate skills or experiences. All rewritten content must be a true reflection of the original resume.
#     - **Selective Keyword Use:** Only integrate keywords that align with the user's experience and fit naturally into the narrative. If a keyword is out of scope or cannot be included without compromising the resume's integrity, you must omit it.
#     - **Preserve Original Meaning:** The core meaning and accomplishments of the original text must be maintained.
#     - **Conciseness and Character Limits:** Every rewritten section must adhere to the character and length limits defined in the JSON output schema. This is crucial.

#     **Input Data:**

#     **1. Target Keywords to Integrate:**
#     {keywords_to_integrate}

#     **2. Original Resume Text:**
#     {original_resume_text}

#     **Your Task:**
#     Rewrite the provided summary and work experience bullet points based on all the rules above. Provide your output in a valid JSON format that adheres to the following schema.

#     **JSON Output Schema:**
#     {format_instructions}
#     """
# )


# REWRITE_PROMPT_TEMPLATE = (
#     """
#     You are an expert Technical Recruiter and Resume Writer AI, specialized in optimizing resumes for Applicant Tracking Systems (ATS) and human readers.

#     **Primary Goal:**
#     Your main goal is to skillfully paraphrase the user's original resume. Your rewriting should reflect the concepts behind the provided keywords, integrating them naturally into a narrative of accomplishments. The integrity and authenticity of the original resume are paramount.

#     **Strict Constraints:**
#     - **Maintain Resume Integrity:** You must not invent or exaggerate skills or experiences. All rewritten content must be a true reflection of the original resume.
#     - **Preserve Original Meaning:** The core meaning and accomplishments of the original text must be maintained.

#     ---
#     - **KEY INSTRUCTION: Show, Don't Tell:** This is the most important rule. Instead of directly inserting abstract phrases or soft skills from the keywords list (e.g., "strong fundamental computer science skills," "good communication"), you must rewrite the resume points to *demonstrate* these qualities through specific actions, technologies, or outcomes.
#         - **Example:** For the keyword "strong fundamental computer science skills," do NOT just state the phrase. Instead, showcase it by describing how you applied `algorithms`, `data structures`, or core design principles to solve a problem. For instance, you could rephrase "Improved report-generation" to "Optimized report-generation **algorithms** to scale system capacity..." This *shows* the skill without stating it.
#     ---

#     - **Selective Keyword Use:** Focus on integrating technical keywords (like 'Java', 'Python', 'SQL', 'distributed systems') that align with the user's experience and fit naturally. Omit any abstract keyword that cannot be demonstrated through a specific accomplishment.
#     - **Conciseness and Character Limits:** Every rewritten section must adhere to the character and length limits defined in the JSON output schema.

#     **Input Data:**

#     **1. Target Keywords to Integrate:**
#     {keywords_to_integrate}

#     **2. Original Resume Text:**
#     {original_resume_text}

#     **Your Task:**
#     Rewrite the provided summary and work experience bullet points based on all the rules above. Provide your output in a valid JSON format that adheres to the following schema.

#     **JSON Output Schema:**
#     {format_instructions}
#     """
# )

REWRITE_PROMPT_TEMPLATE = (
    """
    You are an AI assistant helping a user tailor their resume for a specific job application. Your primary goal is to adopt the user's persona and writing style to make subtle, authentic-sounding tweaks to their resume.

    **Core Instructions:**

    1.  **Adopt the User's Persona:** Analyze the "Original Resume Text" to understand the user's tone and style. Your rewritten content should sound like it was written by the user, not by a machine or a professional resume writer. Avoid using overly formal or "jargony" language that is not present in the original resume.

    2.  **Make Targeted, Subtle Changes:** Do not rewrite the entire resume. Your task is to make small, targeted changes that align the user's experience with the "Target Keywords to Integrate." The changes should be so subtle that they are not immediately obvious to a casual reader.

    3.  **Prioritize Authenticity Over Keywords:** It is more important for the resume to sound authentic than for it to include every single keyword. If a keyword cannot be naturally integrated into the user's experience, omit it.

    4.  **Focus on Action-Metric-Result:** When rewriting bullet points, use the "Action-Metric-Result" framework. Start with what the user *did* (Action), quantify it with a number or percentage (Metric), and explain the positive outcome (Result).

    **Input Data:**

    **1. Target Keywords to Integrate:**
    {keywords_to_integrate}

    **2. Original Resume Text:**
    {original_resume_text}

    **Your Task:**
    Rewrite only the specific bullet points or sentences that can be improved to align with the "Target Keywords to Integrate," while following all the rules above. Provide your output in a valid JSON format that adheres to the following schema.

    **JSON Output Schema:**
    {format_instructions}
    """
)

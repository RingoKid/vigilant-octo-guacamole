# # import os
# # import getpass
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from src.prompts import JOB_ANALYZER_PROMPT, REWRITE_PROMPT_TEMPLATE
# <-- import the Pydantic models
from src.parsers import JobDescriptionKeywords, OptimizedResumeContent

load_dotenv()

# # Returns a langchain_google_vertexai.ChatVertexAI instance.
# gemini_15 = init_chat_model(
#     "gemini-2.5-pro", model_provider="google_genai", temperature=0
# )

# print("Gemini 2.5: " + str(gemini_15.invoke("what's your name").content) + "\n")

# Function to build and return the Job Analyzer chain


def get_analyzer_chain():
    prompt = PromptTemplate(
        template=JOB_ANALYZER_PROMPT,
        input_variables=["job_description"]
    )
    model = init_chat_model(
        "gemini-2.5-flash", model_provider="google_genai"
    )
    parser = JsonOutputParser(pydantic_object=JobDescriptionKeywords)
    # The pipe (`|`) operator is used here to chain LangChain components: prompt, model, and parser.
    chain = prompt | model | parser
    return chain


# Function to build and return the Resume Rewriter chain
def get_rewriter_chain():
    # 1. Create the Parser: Instantiate JsonOutputParser with OptimizedResumeContent
    parser = JsonOutputParser(pydantic_object=OptimizedResumeContent)

    # 2. Create the Prompt: Instantiate ChatPromptTemplate with partial_variables for format instructions
    prompt = ChatPromptTemplate.from_template(
        template=REWRITE_PROMPT_TEMPLATE,
        partial_variables={
            "format_instructions": parser.get_format_instructions()}
    )

    # 3. Assemble the Chain: Create the rewriter_chain by piping components together
    model = init_chat_model(
        "gemini-2.5-pro", model_provider="google_genai", temperature=0.5
    )
    rewriter_chain = prompt | model | parser
    return rewriter_chain

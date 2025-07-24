# # import os
# # import getpass
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from src.prompts import JOB_ANALYZER_PROMPT

load_dotenv()

# # Returns a langchain_google_vertexai.ChatVertexAI instance.
# gemini_15 = init_chat_model(
#     "gemini-2.5-pro", model_provider="google_genai", temperature=0
# )

# print("Gemini 2.5: " + str(gemini_15.invoke("what's your name").content) + "\n")

# Function to build and return the Job Analyzer chain


def get_analyzer_chain():
    load_dotenv()
    prompt = PromptTemplate(
        template=JOB_ANALYZER_PROMPT,
        input_variables=["job_description"]
    )
    model = init_chat_model(
        "gemini-2.5-flash", model_provider="google_genai"
    )
    parser = JsonOutputParser()
    # The pipe (`|`) operator is used here to chain LangChain components: prompt, model, and parser.
    chain = prompt | model | parser
    return chain

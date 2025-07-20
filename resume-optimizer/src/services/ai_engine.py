import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


class AIEngine:
    """
    A class to interact with a generative AI model for text analysis.

    This engine is designed to connect to the Google Gemini Pro model,
    send it a job description, and extract a list of relevant keywords.
    """

    def __init__(self):
        """
        Initializes the AIEngine, setting up the model, prompt, and chain.

        It configures the connection to the Google Gemini Pro model and
        prepares the prompt template needed for keyword extraction.
        """
        # Ensure the GEMINI_API_KEY is set in the environment
        if "GEMINI_API_KEY" not in os.environ:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        # 1. Initialize the Google Gemini Pro language model
        # We set a low temperature to get more predictable and focused results.
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro", temperature=0.2, google_api_key=os.getenv("GEMINI_API_KEY"))

        # 2. Define the prompt template
        # This template guides the AI to perform the specific task of
        # identifying keywords from a job description.
        prompt_template = """
        You are an expert at analyzing job descriptions. Your task is to identify the most important keywords from the text provided.
        These keywords should represent the core skills, technologies, and responsibilities.

        Please return the keywords as a single, comma-separated string.

        Job Description:
        {text}

        Keywords:
        """

        # 3. Create a PromptTemplate object from the string
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["text"]
        )

        # 4. Create the LangChain chain
        # The chain links the language model and the prompt together.
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def get_keywords(self, text: str) -> list[str]:
        """
        Analyzes a job description to extract key skills, technologies, and responsibilities.

        Args:
            text: A string containing the job description.

        Returns:
            A list of strings, where each string is a cleaned keyword.
            Returns an empty list if the text is empty or an error occurs.
        """
        if not text:
            print("Warning: Input text is empty. Returning an empty list.")
            return []

        try:
            # Invoke the chain with the provided text
            # The chain will format the prompt, send it to the model, and get the response.
            response = self.chain.invoke({"text": text})

            # The actual output is in the 'text' key of the response dictionary
            if response and 'text' in response:
                keywords_str = response['text'].strip()
                # Split the comma-separated string into a list and trim whitespace
                keywords_list = [keyword.strip()
                                 for keyword in keywords_str.split(',')]
                return keywords_list
            else:
                print("Warning: Received an empty or invalid response from the model.")
                return []

        except Exception as e:
            # Gracefully handle any exceptions during the API call
            print(
                f"An error occurred while communicating with the AI model: {e}")
            return []

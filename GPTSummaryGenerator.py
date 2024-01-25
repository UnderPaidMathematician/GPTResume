from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load the .env file with the API key
load_dotenv()


class GPTSummaryGenerator:
    """Use langchain to generate summary for the given resume."""
    def __init__(self):
        # Initialize the GPT model
        self.llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.7)

    def generate_summary(self, resume):
        prompt_str = f"You are a human resources manager comparing resumes to a job post.\n" \
                     f"This candidate had an ada2 cosine similarity score of {resume.get_ada2_ranking()}.\n" \
                     f"Start by mentioning their score then write a three paragraph summary comparing the candidates\n" \
                     f"resume: {resume.get_resume_text()}\n" \
                     f"and the job post: {resume.get_job_text()}\n\n" \
                     f"Summary:\n"

        # Invoke the model with the prompt string
        try:
            # invoke the llm using the prompt
            result = self.llm.invoke(prompt_str)

            # return the text prompt
            return result.content

        except Exception as e:
            print(f"Error: {e}")








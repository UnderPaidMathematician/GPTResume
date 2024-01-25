import openai
import os
from scipy.spatial.distance import cosine
from Resume import Resume


class Ada2CosineSimilarity:
    def __init__(self):
        # Assumes that the OpenAI API key is stored in the user environment under OPENAI_API_KEY.
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.openai_client = openai.OpenAI()
        self.resume_embedding = None
        self.job_posting_embedding = None

    def get_ada2cosine_similarity(self, resume_text, job_posting_text, resume: Resume):

        # Use the OpenAI API to get embeddings
        resume_embedding_response = self.openai_client.embeddings.create(
            input=resume_text,
            model="text-embedding-ada-002"
        )
        job_posting_embedding_response = self.openai_client.embeddings.create(
            input=job_posting_text,
            model="text-embedding-ada-002"
        )

        # Extract the embeddings
        self.resume_embedding = resume_embedding_response.data[0].embedding
        self.job_posting_embedding = job_posting_embedding_response.data[0].embedding

        # set the resume embedding vector
        resume.set_ada2_resume_vector(self.resume_embedding)

        # Return the cosine similarity
        return 1 - cosine(self.resume_embedding, self.job_posting_embedding)

    def get_resume_embedding(self):
        """Gets the resume embedding vector."""
        return self.resume_embedding

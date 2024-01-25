class Resume(object):
    def __init__(self, resume_path, resume_text, job_text):
        """Class for grouping resume info."""
        self.resume_path = resume_path
        self.resume_text = resume_text
        self.job_text = job_text
        self.ada2_ranking = None
        self.gpt_summary = None
        self.ada2_resume_vector = None

    def set_ada2_resume_vector(self, resume_vector):
        """Set the ada2 resume vector."""
        self.ada2_resume_vector = resume_vector

    def set_ada2_ranking(self, ada2_ranking):
        """Set the Ada-2 ranking for this resume."""
        self.ada2_ranking = ada2_ranking

    def set_gpt_summary(self, gpt_summary):
        """Set the GPT summary for this resume."""
        self.gpt_summary = gpt_summary

    def get_job_text(self):
        """Get the job text."""
        return self.job_text

    def get_resume_text(self):
        """get the resume text."""
        return self.resume_text

    def get_ada2_ranking(self):
        """Get the Ada-2 ranking for this resume."""
        return self.ada2_ranking

    def __lt__(self, other):
        """Less than for sorting, based on ada2_ranking."""
        # Sorting from greatest to least
        return self.ada2_ranking > other.ada2_ranking

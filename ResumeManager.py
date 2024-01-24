from TextExtractor import TextExtractor
from Resume import Resume
import os

class ResumeManager:
    """Manager for batch building resumes based on a directory."""
    def __init__(self, resume_directory, job_post_directory):
        self.job_post_directory = job_post_directory
        self.resume_directory = resume_directory

        # find relevant paths
        job_paths = self.get_all_paths(target_directory=self.job_post_directory)
        resume_paths = self.get_all_paths(target_directory=resume_directory)

        # extract text from the jobpost as well as the resumes.
        self.resume_text_extractor_list = [TextExtractor(p) for p in resume_paths]
        self.job_post_text_extractor = TextExtractor(job_paths[0])

        # builds a list of resumes
        self.resume_list = [
            Resume(
                resume_path=resume_paths[i],
                resume_text=self.resume_text_extractor_list[i].get_text(),
                job_text=self.job_post_text_extractor.get_text()
            ) for i, x in enumerate(resume_paths)]



    def get_all_paths(self, target_directory):
        """Returns a list of paths to all resumes."""
        all_paths = []
        for root, dirs, files in os.walk(target_directory):
            for file in files:
                full_path = os.path.join(root, file)
                all_paths.append(full_path)
        return all_paths

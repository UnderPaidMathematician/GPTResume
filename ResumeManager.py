from TextExtractor import TextExtractor
from Resume import Resume
import os

class ResumeManager:
    """Manager for batch building resumes based on a directory."""
    def __init__(self, resume_directory):
        self.resume_directory = resume_directory
        resume_paths = self.get_all_paths()
        self.text_extractor_list = [TextExtractor(p) for p in resume_paths]
        self.resume_list = [Resume(resume_path=resume_paths[i], resume_text=self.text_extractor_list[i].get_text()) for i, x in enumerate(resume_paths)]

    def get_all_paths(self):
        all_paths = []
        for root, dirs, files in os.walk(self.resume_directory):
            for file in files:
                full_path = os.path.join(root, file)
                all_paths.append(full_path)
        return all_paths

from GPTSummaryGenerator import GPTSummaryGenerator
from ResultGenerator import ResultGenerator
from TextExtractor import TextExtractor
from Ada2CosineSimilarity import Ada2CosineSimilarity
from Resume import Resume
import os


class ResumeManager:
    """Manager for batch building resumes based on a directory. This method """
    def __init__(self, resume_directory, job_post_directory):
        self.job_post_directory = job_post_directory
        self.resume_directory = resume_directory

        # find relevant paths
        job_paths = self.get_all_paths(target_directory=self.job_post_directory)
        resume_paths = self.get_all_paths(target_directory=resume_directory)

        # extract text from the job post as well as the resumes.
        self.resume_text_extractor_list = [TextExtractor(p) for p in resume_paths]
        self.job_post_text_extractor = TextExtractor(job_paths[0])

        # builds a list of resumes
        self.resume_list = [
            Resume(
                resume_path=resume_paths[i],
                resume_text=self.resume_text_extractor_list[i].get_text(),
                job_text=self.job_post_text_extractor.get_text()
            ) for i, x in enumerate(resume_paths)]

        # Setup AdaCosineSimilarity
        ada2CosineSimilarity = Ada2CosineSimilarity()

        # Assign similarity scores to Resumes
        [
            r.set_ada2_ranking(
                ada2CosineSimilarity.get_ada2cosine_similarity(
                    resume_text=r.get_resume_text(),
                    job_posting_text=r.get_job_text(),
                    resume=r
                ),
            )
            for r in self.resume_list
        ]

        # sort the resume list by ada score. (using the less than magic method)
        self.resume_list.sort()

        # Setup and retrieve the gpt summary using langchain for the top 3 candidates
        gpt_summary_generator = GPTSummaryGenerator()

        # calculate and set the langchain gpt summary for the top 3 candidates
        [r.set_gpt_summary(gpt_summary_generator.generate_summary(r)) for r in self.resume_list[:3]]

        # Generate the resume results
        result_generator = ResultGenerator(folder_path=r'C:\PythonProjects\GPTResume\GPTResume\Results')
        [result_generator.process_resume(resume=r) for r in self.resume_list[:3]]

    @staticmethod
    def get_all_paths(target_directory):
        """Returns a list of paths to all resumes."""
        all_paths = []
        for root, dirs, files in os.walk(target_directory):
            for file in files:
                full_path = os.path.join(root, file)
                all_paths.append(full_path)
        return all_paths

import os
import shutil
import Resume

class ResultGenerator:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self._prepare_folder()

    def _prepare_folder(self):
        # Check if the folder is 'Resumes' or 'JobPost'
        if os.path.basename(self.folder_path) in ['Resumes', 'JobPost']:
            raise ValueError("Cannot use 'Resumes' or 'JobPost' folder with ResultGenerator")

        # Check if folder exists
        if os.path.exists(self.folder_path):
            # Remove all contents of the folder
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            # Create the folder if it does not exist
            os.makedirs(self.folder_path, exist_ok=True)

        print(f"Folder prepared at: {self.folder_path}")

    def process_resume(self, resume: Resume):
        """Processes the resume by copying it to the results folder and generating a readable summary."""

        # Copy the resume file to the results folder
        resume_filename = os.path.basename(resume.resume_path)
        destination_path = os.path.join(self.folder_path, resume_filename)
        shutil.copy(resume.resume_path, destination_path)

        # Create a summary text document
        summary_filename = os.path.splitext(resume_filename)[0] + '_summary.txt'
        summary_path = os.path.join(self.folder_path, summary_filename)

        with open(summary_path, 'w', encoding='utf-8') as summary_file:
            # write the summary to file
            summary_file.write(resume.gpt_summary + "\n\n")

        print(f"Processed resume: {resume_filename}")
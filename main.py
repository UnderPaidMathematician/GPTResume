from ResumeManager import ResumeManager
import os

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the paths relative to the script directory
resume_directory = os.path.join(script_directory, 'Resumes')
job_directory = os.path.join(script_directory, 'JobPost')

# Resume Manager builds the results and holds the results in Resume objects.
resume_manager = ResumeManager(resume_directory=resume_directory, job_post_directory=job_directory)

print('Resume scores vector:')
print([r.get_ada2_ranking() for r in resume_manager.resume_list])
print("Finished Processing Resume Files. See results in the Results folder.")

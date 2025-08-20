from learnen.interview.model_answer import InterviewSaver

if __name__ == "__main__":
    extractor = InterviewSaver(
        resume_path = "data/resume.txt",
        requirements_path = "data/recuiting_requirements_01.txt",
    )
    extractor.run()

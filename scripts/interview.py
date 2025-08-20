from learnen.interview.main import InterviewQuestionGenerator

if __name__ == "__main__":
    extractor = InterviewQuestionGenerator(
        resume_path = "data/resume.txt",
        requirements_path = "data/recuiting_requirements_01.txt",
    )
    extractor.run()

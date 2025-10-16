from learnen.interview.main import InterviewQuestionGenerator

if __name__ == "__main__":
    extractor = InterviewQuestionGenerator(
        resume_path = "data/resume.txt",
        requirements_path = "data/interview/02/recruiting_requirements_02.txt",
    )
    extractor.run()

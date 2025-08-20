from learnen.interview.eval import InterviewEvaluator

if __name__ == "__main__":
    evaluator = InterviewEvaluator(
        input_path="data/interview_answers.json",
        output_path="output/interview/interview_results.json"
    )
    evaluator.run()

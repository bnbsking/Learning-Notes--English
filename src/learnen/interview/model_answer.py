import json
import os
import time

from ..utils.prompts_interview import (
    get_model_answer
)
from ..utils.api import Gemini


class InterviewSaver:
    def __init__(
            self,
            resume_path: str,
            requirements_path: str,
            question_json_path: str = "output/interview/interview_questions.json",
            output_path: str = "output/interview/interview_questions_with_model_answers.json",
            model: str = "gemini-2.0-flash-lite"
        ):
            self.resume_path = resume_path
            self.requirements_path = requirements_path
            self.question_json_path = question_json_path
            self.output_path = output_path
            self.model = Gemini(model)

    def load_txt(self, txt_path: str) -> str:
        with open(txt_path, "r", encoding="utf-8") as f:
            txt = f.read()
        return txt

    def generate_answer(self, requirements: str, resume: str, qa_pairs: list[dict], output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        for i in range(len(qa_pairs)):
            print(f"processing question {i + 1}/{len(qa_pairs)}")
            if qa_pairs[i]["question"] == "===":
                resp = "==="
            else:
                prompt = get_model_answer.strip(" \n") \
                    .replace("{{ recruiting_requirements }}", requirements) \
                    .replace("{{ candidate_resume }}", resume) \
                    .replace("{{ interview_question }}", qa_pairs[i]["question"])
                resp = self.model.run(prompt=prompt)
            qa_pairs[i]["model_answer"] = resp
            time.sleep(3)
        json.dump(
            qa_pairs,
            open(output_path, "w", encoding="utf-8"),
            ensure_ascii = False,
            indent = 4
        )

    def run(self):
        requirements = self.load_txt(self.requirements_path)
        resume = self.load_txt(self.resume_path)
        qa_pairs = json.loads(open(self.question_json_path, "r", encoding="utf-8").read())
        self.generate_answer(requirements, resume, qa_pairs, self.output_path)
        print("Generate complete")
    
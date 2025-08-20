import json
import os

from ..utils.prompts_interview import (
    gen_q_from_requirements,
    gen_q_from_requirements_and_resume
)
from ..utils.api import Gemini


class InterviewQuestionGenerator:
    def __init__(
            self,
            resume_path: str,
            requirements_path: str,
            output_path: str = "output/interview/interview_questions.json",
            model: str = "gemini-2.0-flash-lite"
        ):
            self.resume_path = resume_path
            self.requirements_path = requirements_path
            self.output_path = output_path
            self.model = Gemini(model)

    def load_txt(self, txt_path: str) -> str:
        with open(txt_path, "r", encoding="utf-8") as f:
            txt = f.read()
        return txt

    def generate_q(self, requirements: str, resume: str, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        prompt_req = gen_q_from_requirements.strip(" \n") \
            .replace("{{ recruiting_requirements }}", requirements)
        resp_req = self.model.run(prompt=prompt_req)
        resp_req_json_str = resp_req.replace("```", "").replace("json", "").strip("\n")

        prompt_both = gen_q_from_requirements_and_resume.strip(" \n") \
            .replace("{{ recruiting_requirements }}", requirements) \
            .replace("{{ candidate_resume }}", resume)
        resp_both = self.model.run(prompt=prompt_both)
        resp_both_json_str = resp_both.replace("```", "").replace("json", "").strip("\n")

        try:
            req_q_list = json.loads(resp_req_json_str)
            both_q_list = json.loads(resp_both_json_str)
            qs = []
            for i, q in enumerate(req_q_list + both_q_list):
                qs.append({"id": i, "question": q, "answer": "", "model_answer": "", "eval": "", "score": -1})
            json.dump(
                qs,
                open(output_path, "w", encoding="utf-8"),
                ensure_ascii = False,
                indent = 4
            )
        except Exception as e:
            raise ValueError(f"Error: {e}, resp_req = {resp_req}, resp_both = {resp_both}")

    def run(self):
        requirements = self.load_txt(self.requirements_path)
        resume = self.load_txt(self.resume_path)
        self.generate_q(requirements, resume, self.output_path)
        print("Generate complete")

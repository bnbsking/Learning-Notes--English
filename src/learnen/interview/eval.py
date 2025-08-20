import json
import os

from ..utils.prompts_interview import evaluation
from ..utils.api import Gemini


class InterviewEvaluator:
    def __init__(
            self,
            input_path: str,
            output_path: str,
            max_avg_score: int = 2,
            model: str = "gemini-2.0-flash-lite"
        ):
            self.input_path = input_path
            self.output_path = output_path
            self.max_avg_score = max_avg_score
            self.model = Gemini(model)

    def load_json(self, txt_path: str) -> list[dict]:
        with open(txt_path, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
        return data_dict

    def process_avg_score(self, eval_dict: dict) -> float:
        sumv, eff = 0, 0
        for v in eval_dict.values():
            if str(v).isnumeric():
                sumv += int(v)
                eff += 1
        return sumv / eff if eff > 0 else -1

    def evals(self, data_dict: list[dict], output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        sumv, eff = 0, 0
        for i in range(len(data_dict)):
            print(f"Processing question {i + 1}/{len(data_dict)}")
            prompt = evaluation.strip(" \n") \
                .replace("{{ question }}", data_dict[i]["question"]) \
                .replace("{{ answer }}", data_dict[i]["answer"])
            response = self.model.run(prompt=prompt)
            response_json_str = response.replace("```", "").replace("json", "").strip("\n")

            try:
                response_json = json.loads(response_json_str)
                data_dict[i]["eval"] = response_json
                data_dict[i]["score"] = self.process_avg_score(response_json)
                sumv += data_dict[i]["score"]
                eff += 1
            except Exception as e:
                print(f"Error: {e}, response_json_str = {response_json_str}")
                data_dict[i]["eval"] = response_json_str + "\n" + str(e)
                data_dict[i]["score"] = -1

        json.dump(
            data_dict,
            open(output_path, "w", encoding="utf-8"),
            ensure_ascii = False,
            indent = 4
        )
        print(f"average score = {round(sumv / (eff + 1e-10) / self.max_avg_score, 3)}")
        print(f"average effective = {eff}/{len(data_dict)} = {round(eff / (len(data_dict) + 1e-10), 3)}")

    def run(self):
        data_dict = self.load_json(self.input_path)
        self.evals(data_dict, self.output_path)
        print("Evaluation complete")

import json
import os

from TTS.api import TTS


class QuestionToVoice:
    def __init__(
            self,
            input_path: str = "output/interview/interview_questions.json",
            output_dir: str = "output/interview/interview_audio",
        ):
        self.input_path = input_path
        self.output_dir = output_dir
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

    def read_data(self, input_path: str) -> list:
        with open(input_path, "r", encoding="utf-8") as f:
            qa_pairs = json.load(f)
        return qa_pairs

    def qas_to_audio(self, qa_pairs: list, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        for qa_pair in qa_pairs:
            output_path = f"{output_dir}/qa_question_{qa_pair['id']}.wav"
            if qa_pair["question"] == "===" or os.path.exists(output_path):
                continue
            print(f"Processing question {qa_pair['id'] + 1}/{len(qa_pairs)}")
            self.tts.tts_to_file(text=qa_pair["question"], file_path=output_path)

    def run(self):
        qa_pairs = self.read_data(self.input_path)
        self.qas_to_audio(qa_pairs, self.output_dir)

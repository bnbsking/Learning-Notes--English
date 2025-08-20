import glob
import json
import os
import shutil
import time

from .utils.prompt import extract_vocabs
from .utils.api import Gemini


class ExtractVocab:
    def __init__(
            self,
            input_path: str = "data_tmp.txt",
            accum_content_capacity: int = 16000,  # max 4096 tokens, gemini 1 token ~ 4 characters -> 16384 character
            output_path: str = "output/vocab_tmp.json",
            gemini_model: str = "gemini-2.0-flash-lite"
        ):
        self.input_path = input_path
        self.accum_content_capacity = accum_content_capacity
        self.output_path = output_path
        self.model = Gemini(gemini_model)

    def read_txt_to_list_str(self, input_path: str) -> list[str]:
        with open(input_path, "r", encoding="utf-8") as f:
            blocks = f.read().split("\n\n")
        return blocks

    def extract_vocab_and_save_chunk(self, accum_content: str, save_path: str):
        prompt = extract_vocabs.strip(" \n").replace("{{ vocabularies }}", accum_content)
        resp = self.model.run(prompt=prompt)
        output_json_str = resp.replace("```", "").replace("json", "").strip("\n")
        open(f"{save_path}.txt", "w").write(output_json_str)
        try:
            json.dump(
                json.loads(output_json_str),
                open(f"{save_path}.json", "w", encoding="utf-8"),
                ensure_ascii = False,
                indent = 4
            )
        except Exception as e:
            print(f"Error at chunk {save_path}: {e}")

    def process_to_chunks_and_save(self, blocks: list[str], save_dir: str):
        accum_content, chunk_id = "", 0
        for i in range(len(blocks)):
            if len(accum_content) + len(blocks[i]) + 2 > self.accum_content_capacity:
                print(f"Processing chunk: {chunk_id}")
                self.extract_vocab_and_save_chunk(accum_content, f"{save_dir}/vocab_{chunk_id}")
                time.sleep(5)
                accum_content = ""
                chunk_id += 1
            accum_content += blocks[i] + "\n\n"
        if accum_content:
            print(f"Processing final chunk: {chunk_id}")
            self.extract_vocab_and_save_chunk(accum_content, f"{save_dir}/vocab_{chunk_id}")

    def merge_chunks_and_save(self, json_glob_path: str, output_path: str):
        merged_vocabs = []
        for json_path in glob.glob(json_glob_path):
            with open(json_path, "r", encoding="utf-8") as f:
                vocabs = json.load(f)
                merged_vocabs.extend(vocabs)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(merged_vocabs, f, ensure_ascii=False, indent=4)

    def run(self):
        blocks = self.read_txt_to_list_str(self.input_path)
        tmp_dir = os.path.join(self.output_path, "..", ".tmp_vocab")
        os.makedirs(tmp_dir, exist_ok=True)
        self.process_to_chunks_and_save(blocks, tmp_dir)
        self.merge_chunks_and_save(f"{tmp_dir}/*.json", self.output_path)
        shutil.rmtree(tmp_dir)

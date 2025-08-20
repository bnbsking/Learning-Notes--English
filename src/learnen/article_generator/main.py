import glob
import json
import os
import random
import re
import time

from ..utils.prompt import generate_article
from ..utils.api import Gemini


class ArticleGenerator:
    def __init__(
            self,
            vocab_size: int = 50,
            input_path: str = "output/vocab_tmp.json",
            output_dir: str = "output/articles",
            model: str = "gemini-2.0-flash-lite"
        ):
            self.vocab_size = vocab_size
            self.input_path = input_path
            self.output_dir = output_dir
            self.model = Gemini(model)

    def load_vocab_list(self) -> list[str]:
        with open(self.input_path, "r", encoding="utf-8") as f:
            vocab_list = json.load(f)
        return vocab_list

    def get_start_idx(self, glob_path: str, extract_idx_pattern: str) -> int:
        max_idx = 0
        for md_path in glob.glob(glob_path):
            match = re.search(extract_idx_pattern, md_path)
            idx = int(match.group(1)) if match else -1
            max_idx = max(max_idx, idx)
        return max_idx + 1

    def generate_articles_and_save(self, vocab_groups: list[list[str]], start_idx: int, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        for i, vocab_group in enumerate(vocab_groups):
            print(f"Generating article for group {i + 1}/{len(vocab_groups)}")
            prompt = generate_article.strip(" \n").replace("{{ vocabularies }}", json.dumps(vocab_group, ensure_ascii=False))
            response = self.model.run(prompt=prompt)
            output_path = os.path.join(output_dir, f"article_{i + start_idx}.md")
            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(response)
            time.sleep(5)

    def run(self):
        vocab_list = self.load_vocab_list()
        random.shuffle(vocab_list)
        vocab_groups = [vocab_list[i: i + self.vocab_size] for i in range(0, len(vocab_list), self.vocab_size)]
        start_idx = self.get_start_idx(f"{self.output_dir}/article_*.md", r"article_(\d+).md")
        self.generate_articles_and_save(vocab_groups, start_idx, self.output_dir)

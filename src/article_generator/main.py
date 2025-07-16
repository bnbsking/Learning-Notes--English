import os
import random
import re
import glob
import json
import time

from ..utils.prompt import generate_article
from ..utils.api import Gemini


VOCAB_SIZE = 50
INPUT_PATH = "output/vocab.json"
OUTPUT_DIR = "output/articles"
MODEL = "gemini-2.0-flash-lite"


def path_to_idx(path: str) -> int:
    match = re.search(r"article_(\d+).md", path)
    if match:
        return int(match.group(1)) + 1
    else:
        return 0


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        vocabs = json.load(f)
    
    random.shuffle(vocabs)
    groups = [vocabs[i:i + VOCAB_SIZE] for i in range(0, len(vocabs), VOCAB_SIZE)]

    model = Gemini(MODEL)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    start_idx = max([0] + [path_to_idx(p) for p in glob.glob(f"{OUTPUT_DIR}/article_*.md") ])

    for i in range(len(groups)):
        vocab_group = groups[i]
        prompt = generate_article.strip(" \n").replace("{{ vocabularies }}", json.dumps(vocab_group, ensure_ascii=False))
        
        print(f"Generating article for group {i + 1}/{len(groups)}")
        response = model.run(prompt=prompt)
        
        output_path = os.path.join(OUTPUT_DIR, f"article_{i + start_idx}.md")
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(response)
        
        time.sleep(10)

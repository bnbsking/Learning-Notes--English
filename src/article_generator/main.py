import os
import random
import json
import time

from ..utils.prompt import generate_article
from ..utils.api import Gemini


VOCAB_SIZE = 50
INPUT_PATH = "output/vocab.json"
OUTPUT_DIR = "output/articles"
MODEL = "gemini-2.0-flash-lite"


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        vocabs = json.load(f)
    
    random.shuffle(vocabs)
    groups = [vocabs[i:i + VOCAB_SIZE] for i in range(0, len(vocabs), VOCAB_SIZE)]

    model = Gemini(MODEL)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in range(len(groups)):
        vocab_group = groups[i]
        prompt = generate_article.strip(" \n").replace("{{ vocabularies }}", json.dumps(vocab_group, ensure_ascii=False))
        
        print(f"Generating article for group {i + 1}/{len(groups)}")
        response = model.run(prompt=prompt)
        
        output_path = os.path.join(OUTPUT_DIR, f"article_{i + 1}.md")
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(response)
        
        time.sleep(10)

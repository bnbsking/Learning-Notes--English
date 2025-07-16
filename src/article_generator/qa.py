import os
import glob
import re
import time

from ..utils.prompt import generate_article_qa
from ..utils.api import Gemini


INPUT_DIR = "output/articles"
OUTPUT_DIR = "output/articles"
MODEL = "gemini-2.0-flash-lite"


if __name__ == "__main__":
    model = Gemini(MODEL)

    for path in sorted(glob.glob(os.path.join(INPUT_DIR, "article_*.md"))):
        article_id = re.findall(r"article_(\d+)\.md", path)[0]

        with open(path, "r", encoding="utf-8") as f:
            article = f.read()

        if "=" * 70 in article:
            #print(f"Article {article_id} already has Q&A, skipping.")
            continue
        else:
            print(f"Processing article {article_id}...")

        prompt = generate_article_qa.strip(" \n").replace("{{ article }}", article)
        
        response = model.run(prompt=prompt)

        content = article + "\n\n" + "=" * 70 + "\n\n" + response

        output_path = os.path.join(OUTPUT_DIR, os.path.basename(path))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        time.sleep(10)

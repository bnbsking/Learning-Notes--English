import glob
import os
import re
import time

from ..utils.prompts_en import generate_article_qa
from ..utils.api import Gemini


class ArticleGeneratorQA:
    def __init__(
        self,
        input_dir: str = "output/articles",
        output_dir: str = "output/articles",
        model: str = "gemini-2.0-flash-lite"
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.model = Gemini(model)

    def add_qa(self, article: str) -> str:
        prompt = generate_article_qa.strip(" \n").replace("{{ article }}", article)
        response = self.model.run(prompt=prompt)
        article = article + "\n\n" + "=" * 70 + "\n\n" + response
        return article

    def run(self):
        for path in sorted(glob.glob(os.path.join(self.input_dir, "article_*.md"))):
            with open(path, "r", encoding="utf-8") as f:
                article = f.read()
            if "=" * 70 in article:
                continue

            article_id = re.findall(r'article_(\d+)\.md', path)[0]
            print(f"Processing article article_id = {article_id}...")
            content = self.add_qa(article)
            output_path = os.path.join(self.output_dir, os.path.basename(path))
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            time.sleep(10)

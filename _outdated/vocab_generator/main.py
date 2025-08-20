import os
import glob
import json
import time

from ..utils.prompt import generate_vocab
from ..utils.api import Gemini


VOCAB_SIZE = 10
INPUT_PATH = "output/vocab.json"
OUTPUT_DIR = "output/vocab_details"
MODEL = "gemini-2.0-flash-lite"
TOPN = 0


if __name__ == "__main__":
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        vocabs = json.load(f)
    
    groups = [vocabs[i: i + VOCAB_SIZE] for i in range(0, len(vocabs), VOCAB_SIZE)]

    model = Gemini(MODEL)
    tmp_dir = os.path.join(OUTPUT_DIR, "tmp_vocab_detail")
    os.makedirs(tmp_dir, exist_ok=True)

    for chunk_i in range(min(len(groups), TOPN)):
        vocab_group = groups[chunk_i]
        prompt = generate_vocab.strip(" \n").replace("{{ vocabularies }}", json.dumps(vocab_group, ensure_ascii=False))
        
        print(f"Generating article for chunk {chunk_i + 1}/{len(groups)}")
        response = model.run(prompt=prompt)
        
        out = response.replace("```", "").replace("json", "").strip("\n")
        open(f"{tmp_dir}/vocab_{chunk_i + 1}.txt", "w").write(out)
        try:
            json.dump(
                json.loads(out),
                open(f"{tmp_dir}/vocab_{chunk_i + 1}.json", "w", encoding="utf-8"),
                ensure_ascii=False,
                indent=4
            )
            os.remove(f"{tmp_dir}/vocab_{chunk_i + 1}.txt")
        except Exception as e:
            print(f"Error at chunk {chunk_i}: {e}")
        
        time.sleep(10)
    
    # Merge all vocab chunks
    merged_vocabs = []
    for json_path in glob.glob(f"{tmp_dir}/vocab_*.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            vocabs = json.load(f)
            merged_vocabs += vocabs

    # Save merged vocabularies
    with open(f"{OUTPUT_DIR}/vocab_details.json", "w", encoding="utf-8") as f:
        json.dump(merged_vocabs, f, ensure_ascii=False, indent=4)

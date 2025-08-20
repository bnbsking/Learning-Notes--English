# /Users/james.chao/Library/Application Support/tts/vocoder_models--en--ljspeech--hifigan_v2
# tts_models/en/ljspeech/tacotron2-DDC
# /Users/james.chao/miniconda3/envs/tts/lib/python3.10/site-packages/TTS/tts/configs/tacotron2_config.py
import json, os, multiprocessing
from TTS.api import TTS


INPUT_PATH = "output/vocab_details/vocab_details.json"
OUTPUT_DIR = "output/voice/tmp_voice"


def dict_to_text(d):
    text = ""
    for key, value in d.items():
        text += f"{key}:\n"
        if isinstance(value, list):
            text += "\n".join(value) + "\n"
        else:
            text += f"{value}\n"
    return text.replace("/", ", ")


def run_with_timeout(func, timeout_sec):
    p = multiprocessing.Process(target=func)
    p.start()
    p.join(timeout_sec)

    if p.is_alive():
        print(f"Function exceeded {timeout_sec} seconds. Terminating...")
        p.terminate()
        p.join()


with open(INPUT_PATH, "r", encoding="utf-8") as f:
    L = json.load(f)

os.makedirs(OUTPUT_DIR, exist_ok=True)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

for i in range(1, len(L)):
    print(i)
    text = dict_to_text(L[i])
    #def f():
    #    try:
    tts.tts_to_file(text=text, file_path=f"{OUTPUT_DIR}/{i}.wav")
    #    except Exception as e:
    #        print(f"Error generating voice for vocab {i}: {e}")
    #run_with_timeout(f, 60)

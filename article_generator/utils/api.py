import os
from google import genai
import time


class Gemini:
    models = {
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash",
    }

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    def run(self, prompt: str, retry_times = 10, retry_sec = 10) -> str:
        while retry_times > 0:
            try:
                response = self.client.models.generate_content(
                    model=self.model_name, contents=[prompt]
                )
                return response.text
            except Exception as e:
                print(f"ERROR:", e)
                time.sleep(retry_sec)
                retry_times -= 1

        print("Retry times exhausted !!!")
        return ""

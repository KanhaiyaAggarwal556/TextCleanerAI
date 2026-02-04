import os
import json
from google import genai
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("[ERROR] GOOGLE_API_KEY not found. Check your .env file!")
    exit()

client = genai.Client(api_key=api_key)

def clean_text_file(file_path):
    try:
        with open(file_path, "r") as f:
            raw_text = f.read()
    except FileNotFoundError:
        return None
    prompt = f"""
        You are a data assistant.

        STRICT RULES:
        - Output ONLY valid JSON
        - No markdown
        - No explanations
        - No backticks
        - No extra text

        Required JSON schema:
        {{
        "cpt_codes_identified": [],
        "chronological_summary": []
        }}

        Raw Text:
        {raw_text}
        """

    
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {
                "error": "AI did not return valid JSON",
                "raw_output": response.text
            }

    except Exception as e:
        return f"[ERROR] AI Service Error: {e}"

if __name__ == "__main__":
    try:
        user_filename = input("Write your Text File Name (e.g. trainingData): ").strip()
        
        if not user_filename.endswith(".txt"):
            user_filename += ".txt"

        if not os.path.exists(user_filename):
            with open(user_filename, "w") as f:
                f.write("yo boss, i aint coming in tmrw")

        cleaned_result = clean_text_file(user_filename)

        with open("process.json", "w") as file:
            json.dump(cleaned_result, file, indent=2)
    except Exception as e:
        print(f"[SYSTEM ERROR] {e}")
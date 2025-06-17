import json
import requests
from datetime import datetime
from pathlib import Path

CAPSULE_DIR = "capsules"
LATEST_CAPSULE = sorted(Path(CAPSULE_DIR).glob("capsule_*.json"))[-1]

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def load_latest_capsule():
    with open(LATEST_CAPSULE, "r", encoding="utf-8") as f:
        return json.load(f)

def query_groq_model(context_text, user_question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    prompt = f"""You are a workplace assistant.

Here is the session context:
{context_text}

Now answer this question from the user:
{user_question}
"""

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        content = response.json()
        print("\n🤖 Assistant Response:")
        print(content["choices"][0]["message"]["content"])
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    print("🔁 Resuming last context capsule...\n")

    capsule = load_latest_capsule()
    print(f"📂 Loaded capsule from: {LATEST_CAPSULE}")
    print(f"\n🧠 Capsule Summary:\n{capsule.get('summary', '(No summary)')}\n")
    print(f"📄 Context Size: {len(capsule.get('context', '')) // 4} tokens (approx.)\n")

    question = input("> What would you like to ask the assistant about this session?\n> ").strip()
    if question:
        query_groq_model(capsule["context"], question)

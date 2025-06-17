import streamlit as st
import json
import requests
from pathlib import Path

# Constants
CAPSULE_DIR = "capsules"
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# Load latest capsule file
def load_latest_capsule():
    capsules = sorted(Path(CAPSULE_DIR).glob("capsule_*.json"))
    if not capsules:
        return None, None
    latest = capsules[-1]
    with open(latest, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data, latest.name

# Send query to Groq model
def query_groq_model(context_text, user_question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
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
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f" Error {response.status_code}: {response.text}"

# Streamlit UI
st.set_page_config(page_title="ContextPilot QA", layout="wide")
st.title("ContextPilot: Capsule Query App")

capsule, capsule_name = load_latest_capsule()
if capsule is None:
    st.warning("No capsule found in the 'capsules' directory.")
    st.stop()

with st.expander("Capsule Summary"):
    st.markdown(f"**Filename:** `{capsule_name}`")
    st.markdown(f"**Summary:**\n{capsule.get('summary', '(No summary)')}")
    st.markdown(f"**Context Size:** `{len(capsule.get('context', '')) // 4}` tokens (approx.)")

st.divider()

question = st.text_input("Ask a question about your last session:", placeholder="e.g., What were the limitations of LLMs I noted?")
if st.button("🔍 Submit Query") and question.strip():
    with st.spinner("Querying Groq..."):
        response = query_groq_model(capsule["context"], question.strip())
        st.success("Response received:")
        st.markdown(response)


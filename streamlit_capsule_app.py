import streamlit as st
import json
import requests
from pathlib import Path

# Constants
CAPSULE_DIR = "capsules"
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# Load capsule file
def load_capsule(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f), Path(file_path).name

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
        return f"❌ Error {response.status_code}: {response.text}"

# Streamlit UI
st.set_page_config(page_title="ContextPilot QA", layout="wide")
st.title("🧠 ContextPilot: Capsule Query App")

# Load all capsule files
capsule_files = sorted(Path(CAPSULE_DIR).glob("capsule_*.json"))
if not capsule_files:
    st.warning("No capsules found in the 'capsules' directory.")
    st.stop()

# Dropdown for capsule selection
selected_capsule_file = st.selectbox("📁 Select a capsule to load:", capsule_files, format_func=lambda x: x.name)
capsule, capsule_name = load_capsule(selected_capsule_file)

# Session state for multi-turn chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display capsule info
with st.expander("📄 Capsule Summary"):
    st.markdown(f"**Filename:** `{capsule_name}`")
    st.markdown(f"**Summary:**\n{capsule.get('summary', '(No summary)')}")
    st.markdown(f"**Context Size:** `{len(capsule.get('context', '')) // 4}` tokens (approx.)")

st.divider()

# Question input
question = st.text_input("💬 Ask a question about your selected session:", placeholder="e.g., What were the limitations of LLMs I noted?")
if st.button("🔍 Submit Query") and question.strip():
    with st.spinner("Querying Groq..."):
        response = query_groq_model(capsule["context"], question.strip())
        st.session_state.chat_history.append((question.strip(), response))

# Display chat history
if st.session_state.chat_history:
    st.markdown("## 🗂️ Chat History")
    for idx, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"**Q{idx}:** {q}")
        st.markdown(f"**A{idx}:** {a}")
        st.markdown("---")

st.caption("Built with ❤️ using Streamlit and Groq")

import streamlit as st
from groq import Groq
import datetime

# -------------------------------
# Function to get Groq API response
# -------------------------------
def get_response(messages, model_id="llama-3.1-8b-instant"):
    try:
        groq_api_key = st.secrets["groq_api_key"]
        client = Groq(api_key=groq_api_key)

        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=100,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# -------------------------------
# Streamlit App Configuration
# -------------------------------
st.set_page_config(page_title="Groq Chatbot", page_icon="💬", layout="wide")

# -------------------------------
# Custom Styling
# -------------------------------
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton button {
        border-radius: 6px;
        padding: 0.5em 1em;
        font-weight: 500;
    }
    .stTextInput > div > div > input {
        border-radius: 6px;
    }
    .chat-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Initialize session state
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# Title and Instructions
# -------------------------------
st.title("💬 Groq-Powered Chatbot")
st.caption("Ask me anything. Powered by LLaMA 3 on Groq's ultra-fast inference engine.")

# -------------------------------
# Chat Container
# -------------------------------
chat_container = st.container()

# Display chat history
with chat_container:
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

# -------------------------------
# Chat Input Box
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare messages and get model response
    response = get_response(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

# -------------------------------
# Chat Controls (Export / Clear)
# -------------------------------
st.divider()
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
       

with col2:
    def export_chat():
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_export_{now}.txt"
        chat_lines = []
        for msg in st.session_state.chat_history:
            role = "You" if msg["role"] == "user" else "Bot"
            chat_lines.append(f"{role}: {msg['content']}\n")
        return filename, "\n".join(chat_lines)

    if st.button("📤 Export Chat", use_container_width=True):
        filename, chat_text = export_chat()
        st.download_button(
            label="Download Chat as .txt",
            data=chat_text,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )

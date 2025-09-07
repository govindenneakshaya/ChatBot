import streamlit as st
from groq import Groq

def get_response(messages,model_id="llama-3.1-8b-instant"):
    try:
        groq_api_key = st.secrets["groq_api_key"]

        client = Groq(api_key=groq_api_key)

        formatted_messages = []
        for msg in messages:
            role=msg['role']
            content=msg['content']
            formatted_messages.append({"role": role, "content": content})
        response= client.chat.completions.create(
            model=model_id,
            messages=formatted_messages,
            max_tokens=200,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
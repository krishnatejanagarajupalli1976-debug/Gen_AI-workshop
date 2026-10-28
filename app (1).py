
import streamlit as st
from groq import Groq

st.title("🩺 Health Assistant")
st.caption("Ask health-related questions")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """
You are a Health Assistant.
Answer only health-related questions.
Use simple language.
Do not diagnose diseases or prescribe medicines.
For emergencies, advise immediate medical care.
"""

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear conversation
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get a new question
if question := st.chat_input("Ask a health question..."):

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Send instructions and conversation history
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + st.session_state.messages

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages
            )

            answer = response.choices[0].message.content

        st.write(answer)

    # Save answer for the next turn
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

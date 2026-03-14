import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from personality import personality
from memory import add_user_message, add_ai_message, get_conversation
from profile_memory import load_profile, save_profile

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

profile = load_profile()

st.set_page_config(
    page_title="Zarah AI",
    page_icon="💙",
    layout="wide"
)

# ---------- Custom UI Styling ----------
st.markdown("""
<style>

body {
    background-color: #0f172a;
}

.stChatMessage {
    padding: 12px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Title ---------- 
st.title(" Zarah AI Companion 💙 ")
st.caption("A conversational AI with memory")

# ---------- Chat History ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for role, msg in st.session_state.chat_history:

    if role == "user":
        with st.chat_message("user", avatar="🧑"):
            st.write(msg)

    else:
        with st.chat_message("assistant", avatar="💙"):
            st.write(msg)

# ---------- User Input ----------
user_input = st.chat_input("Type your message...")

if user_input:

    add_user_message(user_input)

    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("user", avatar="🧑"):
        st.write(user_input)

    # ---------- Profile Context ----------
    profile_text = (
        f"User Profile:\n"
        f"Name: {profile['name'] or 'Unknown'}\n"
        f"City: {profile['city'] or 'Unknown'}\n"
        f"Hobbies: {', '.join(profile['hobbies']) if profile['hobbies'] else 'Unknown'}"
    )

    messages = [
        {"role": "system", "content": personality},
        {"role": "system", "content": profile_text}
    ] + get_conversation()[-12:]

    # ---------- AI Response ----------
    with st.spinner("Zarah is thinking..."):

        response = client.chat.completions.create(
            model="mistralai/devstral-2512",
            messages=messages,
            max_tokens=300
        )

    reply = response.choices[0].message.content.strip()

    add_ai_message(reply)

    st.session_state.chat_history.append(("assistant", reply))

    with st.chat_message("assistant", avatar="💙"):
        st.write(reply)

    save_profile(profile)
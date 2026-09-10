import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from personality import personality
from memory import add_user_message, add_ai_message, get_conversation
from profile_memory import load_profile, save_profile

# ---------- Load Environment ----------
load_dotenv()

# Try local .env first
api_key = os.getenv("OPENROUTER_API_KEY")

# If not found, try Streamlit Secrets
if not api_key:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        st.error("❌ OpenRouter API key not found.")
        st.info(
            "Local: Add OPENROUTER_API_KEY to your .env file.\n\n"
            "Streamlit Cloud: Add OPENROUTER_API_KEY in App Settings → Secrets."
        )
        st.stop()

# ---------- OpenRouter Client ----------
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# ---------- Load User Profile ----------
profile = load_profile()

# ---------- Streamlit Config ----------
st.set_page_config(
    page_title="Zarah AI",
    page_icon="💙",
    layout="centered"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>

.stChatMessage {
    padding: 12px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("💙 Zarah AI Companion")
st.caption("A conversational AI with memory")

# ---------- Chat History ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display Previous Messages
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

    # Save user message
    add_user_message(user_input)

    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("user", avatar="🧑"):
        st.write(user_input)

    # ---------- User Profile Context ----------
    profile_text = (
        f"User Profile:\n"
        f"Name: {profile['name'] or 'Unknown'}\n"
        f"City: {profile['city'] or 'Unknown'}\n"
        f"Hobbies: {', '.join(profile['hobbies']) if profile['hobbies'] else 'Unknown'}"
    )

    # ---------- Build Messages ----------
    messages = [
        {"role": "system", "content": personality},
        {"role": "system", "content": profile_text}
    ] + get_conversation()[-12:]

    # ---------- Generate Response ----------
    with st.spinner("💙 Zarah is thinking..."):

        try:
            response = client.chat.completions.create(
                model="inclusionai/ling-3.0-flash-sante:free",
                messages=messages,
                max_tokens=300
            )

            reply = response.choices[0].message.content.strip()

        except Exception as e:
            st.error(f"OpenRouter Error:\n\n{e}")
            st.stop()

    # Save AI response
    add_ai_message(reply)

    st.session_state.chat_history.append(("assistant", reply))

    with st.chat_message("assistant", avatar="💙"):
        st.write(reply)

    # Save Profile
    save_profile(profile)

import os
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

# Load user profile
profile = load_profile()

print("Hello. Zarah here 💙")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Zarah: Bye! Take care! 💙")
        break

    # store user message
    add_user_message(user_input)

    # format profile nicely for the AI
    profile_text = (
        f"User Profile:\n"
        f"Name: {profile['name'] or 'Unknown'}\n"
        f"City: {profile['city'] or 'Unknown'}\n"
        f"Hobbies: {', '.join(profile['hobbies']) if profile['hobbies'] else 'Unknown'}"
    )

    # build conversation
    messages = [
        {"role": "system", "content": personality},
        {"role": "system", "content": profile_text}
    ] + get_conversation()[-12:]

    # API call
    response = client.chat.completions.create(
        model="mistralai/devstral-2512",
        messages=messages,
        max_tokens=300
    )

    reply = response.choices[0].message.content.strip()

    print("Zarah:", reply)

    # store AI response
    add_ai_message(reply)

    # save profile
    save_profile(profile)
conversation = []

def add_user_message(msg):
    conversation.append({"role": "user", "content": msg})

def add_ai_message(msg):
    conversation.append({"role": "assistant", "content": msg})

def get_conversation():
    return conversation
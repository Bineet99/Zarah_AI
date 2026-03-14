import json

FILE = "user_profile.json"

def load_profile():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "name": "",
            "city": "",
            "hobbies": []
        }

def save_profile(profile):
    with open(FILE, "w") as f:
        json.dump(profile, f, indent=2)
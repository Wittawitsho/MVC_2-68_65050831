import json

USER_FILE = "data/users.json"


class UserModel:
    def __init__(self):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            self.users = json.load(f)

    def authenticate(self, user_id):
        return next((u for u in self.users if u["user_id"] == user_id), None)

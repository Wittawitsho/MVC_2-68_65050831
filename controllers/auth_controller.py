from models.user_model import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self.current_user = None

    def login(self, user_id):
        user = self.user_model.authenticate(user_id)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self):
        self.current_user = None

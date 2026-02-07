from controllers.auth_controller import AuthController
from controllers.rumor_controller import RumorController
from controllers.report_controller import ReportController
from models.rumor_model import RumorModel

class AppController:
    def __init__(self):
        self.auth = AuthController()
        self.rumor = RumorController()
        self.report = ReportController()

    # Auth
    @property
    def current_user(self):
        return self.auth.current_user

    def login(self, user_id):
        return self.auth.login(user_id)

    def logout(self):
        self.auth.logout()

    # Rumor
    def get_rumors(self):
        return self.rumor.get_rumors()

    def get_rumor_detail(self, rumor_id):
        return self.rumor.get_rumor_detail(rumor_id)

    def add_rumor(self, title, source):
        return self.rumor.add_rumor(title, source)

    # Report
    def report_rumor(self, rumor_id, report_type):
        user = self.current_user
        return self.report.report_rumor(
            user["user_id"],
            rumor_id,
            report_type,
            self.rumor.model
        )

    # Verify
    def verify_rumor(self, rumor_id, result):
        self.rumor.model.verify_rumor(rumor_id, result)
        return "ยืนยันข่าวเรียบร้อย"

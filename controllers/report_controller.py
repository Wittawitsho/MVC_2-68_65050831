from models.report_model import ReportModel

class ReportController:
    def __init__(self):
        self.model = ReportModel()

    def report_rumor(self, user_id, rumor_id, report_type, rumor_model):
        if self.model.already_reported(user_id, rumor_id):
            return "คุณรายงานข่าวนี้ไปแล้ว"

        self.model.add_report(user_id, rumor_id, report_type)
        rumor_model.increase_report(rumor_id)

        return "รายงานข่าวเรียบร้อย"

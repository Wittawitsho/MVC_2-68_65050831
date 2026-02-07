from models.rumor_model import RumorModel
from datetime import datetime

class RumorController:
    def __init__(self):
        self.model = RumorModel()

    def get_rumors(self):
        return self.model.get_all()

    def get_rumor_detail(self, rumor_id):
        return self.model.get_by_id(rumor_id)

    def add_rumor(self, title, source):
        rumor = {
            "rumor_id": self.model.generate_rumor_id(),
            "title": title,
            "source": source,
            "report_count": 0,
            "status": "normal",
            "date_created": datetime.now().strftime("%Y-%m-%d"),
            "credibility": 0,
        }
        self.model.add_rumor(rumor)
        return "เพิ่มข่าวลือเรียบร้อย"

from datetime import datetime
from models.user_model import UserModel
from models.rumor_model import RumorModel
from models.report_model import ReportModel


class RumorController:
    def __init__(self):
        self.user_model = UserModel()
        self.rumor_model = RumorModel()
        self.report_model = ReportModel()
        self.current_user = None  # เก็บ user ที่ login

    # ---------- AUTH ----------
    def login(self, user_id):
        user = self.user_model.authenticate(user_id)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self):
        self.current_user = None

    # ---------- RUMOR ----------
    def get_rumors(self):
        return self.rumor_model.get_all()

    def get_rumor_detail(self, rumor_id):
        return self.rumor_model.get_by_id(rumor_id)

    def report_rumor(self, rumor_id, report_type):
        if self.current_user["role"] == "checker":
            return "ผู้ตรวจสอบไม่สามารถรายงานข่าวได้"

        rumor = self.rumor_model.get_by_id(rumor_id)

        if rumor["status"] == "verified":
            return "ข่าวนี้ถูกยืนยันแล้ว"

        user_id = self.current_user["user_id"]

        if self.report_model.already_reported(user_id, rumor_id):
            return "ไม่สามารถรายงานซ้ำได้"

        self.report_model.add_report(user_id, rumor_id, report_type)
        self.rumor_model.increase_report(rumor_id)
        return "รายงานสำเร็จ"


    def verify_rumor(self, rumor_id, result):
        if self.current_user["role"] != "checker":
            return "คุณไม่มีสิทธิ์ยืนยันข่าว"

        self.rumor_model.verify_rumor(rumor_id, result)

        if result == "true":
            return "ยืนยันแล้ว: ข่าวเป็นข้อมูลจริง"
        else:
            return "ยืนยันแล้ว: ข่าวเป็นข้อมูลเท็จ"
        
    def add_rumor(self, title, source):
        new_id = self.rumor_model.generate_rumor_id()

        rumor = {
            "rumor_id": new_id,
            "title": title,
            "source": source,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "credibility": 0,
            "report_count": 0,
            "status": "normal",
            "verified_result": None
        }

        self.rumor_model.add_rumor(rumor)
        return "เพิ่มข่าวลือเรียบร้อย (ยังไม่ผ่านการตรวจสอบ)"
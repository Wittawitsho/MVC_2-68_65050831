from models.rumor_model import RumorModel

class VerifyController:
    def __init__(self, current_user):
        self.current_user = current_user
        self.rumor_model = RumorModel()

    def verify_rumor(self, rumor_id, result):
        if self.current_user["role"] != "checker":
            return "คุณไม่มีสิทธิ์ยืนยันข่าว"

        self.rumor_model.verify_rumor(rumor_id, result)

        if result == "true":
            return "ยืนยันแล้ว: ข่าวเป็นข้อมูลจริง"
        else:
            return "ยืนยันแล้ว: ข่าวเป็นข้อมูลเท็จ"

import json
from datetime import datetime

RUMOR_FILE = "data/rumors.json"
PANIC_THRESHOLD = 3  # เกิน 3 รายงาน = panic


class RumorModel:
    def __init__(self):
        self.rumors = self._load()

    def _load(self):
        with open(RUMOR_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self):
        with open(RUMOR_FILE, "w", encoding="utf-8") as f:
            json.dump(self.rumors, f, ensure_ascii=False, indent=2)

    def get_all(self):
        return self.rumors

    def get_by_id(self, rumor_id):
        return next((r for r in self.rumors if r["rumor_id"] == rumor_id), None)

    def increase_report(self, rumor_id):
        rumor = self.get_by_id(rumor_id)
        if rumor and rumor["status"] != "verified":
            rumor["report_count"] += 1
            if rumor["report_count"] >= PANIC_THRESHOLD:
                rumor["status"] = "panic"
            self._save()

    def verify_rumor(self, rumor_id, result):
        """
        result: 'true' หรือ 'false'
        """
        rumor = self.get_by_id(rumor_id)
        if rumor:
            rumor["status"] = "verified"
            rumor["verified_result"] = result
            self._save()
    
    def generate_rumor_id(self):
        ids = [
            int(r["rumor_id"])
            for r in self.rumors
            if "rumor_id" in r
        ]

        if not ids:
            return "10000001"

        return str(max(ids) + 1)
    
    def add_rumor(self, rumor):
        self.rumors.append(rumor)
        self._save()
import json
from datetime import datetime

REPORT_FILE = "data/reports.json"


class ReportModel:
    def __init__(self):
        self.reports = self._load()

    def _load(self):
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self):
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.reports, f, ensure_ascii=False, indent=2)

    def already_reported(self, user_id, rumor_id):
        return any(
            r for r in self.reports
            if r["user_id"] == user_id and r["rumor_id"] == rumor_id
        )

    def add_report(self, user_id, rumor_id, report_type):
        self.reports.append({
            "user_id": user_id,
            "rumor_id": rumor_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": report_type
        })
        self._save()

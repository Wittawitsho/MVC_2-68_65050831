class SummaryController:
    def __init__(self, rumor_model):
        self.rumor_model = rumor_model

    def get_summary(self):
        rumors = self.rumor_model.get_all()

        return {
            "panic": [r for r in rumors if r["status"] == "panic"],
            "true": [
                r for r in rumors
                if r["status"] == "verified" and r["verified_result"] == "true"
            ],
            "false": [
                r for r in rumors
                if r["status"] == "verified" and r["verified_result"] == "false"
            ]
        }

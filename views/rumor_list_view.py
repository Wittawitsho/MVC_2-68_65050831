import tkinter as tk
from views.rumor_detail_view import RumorDetailView


class RumorListView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.title("รวมข่าวลือ")

        rumors = controller.get_rumors()
        rumors.sort(key=lambda x: x["report_count"], reverse=True)
        
        for r in rumors:
            btn = tk.Button(
                self,
                text=f'{r["title"]} (Reports: {r["report_count"]})',
                command=lambda rid=r["rumor_id"]:
                    RumorDetailView(self, controller, rid)
            )
            btn.pack(fill="x", padx=10, pady=3)

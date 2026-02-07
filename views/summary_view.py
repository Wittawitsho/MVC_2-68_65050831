import tkinter as tk


class SummaryView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.title("สรุปผล")

        rumors = controller.get_rumors()

        # ---------- PANIC ----------
        tk.Label(self, text="ข่าวลือสถานะ PANIC", fg="red").pack()
        for r in rumors:
            if r["status"] == "panic":
                tk.Label(self, text=r["title"]).pack(anchor="w")

        # ---------- VERIFIED TRUE ----------
        tk.Label(self, text="\nข่าวที่ยืนยันว่าเป็นข้อมูลจริง", fg="green").pack()
        for r in rumors:
            if r["status"] == "verified" and r["verified_result"] == "true":
                tk.Label(self, text=r["title"]).pack(anchor="w")

        # ---------- VERIFIED FALSE ----------
        tk.Label(self, text="\nข่าวที่ยืนยันว่าเป็นข้อมูลเท็จ", fg="red").pack()
        for r in rumors:
            if r["status"] == "verified" and r["verified_result"] == "false":
                tk.Label(self, text=r["title"]).pack(anchor="w")

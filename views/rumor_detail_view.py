import tkinter as tk
from tkinter import messagebox


class RumorDetailView(tk.Toplevel):
    def __init__(self, master, controller, rumor_id):
        super().__init__(master)
        self.controller = controller
        self.rumor_id = rumor_id
        self.title("รายละเอียดข่าวลือ")
        self.report_type_var = tk.StringVar(value="ข้อมูลเท็จ")
        self.refresh()

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()

        rumor = self.controller.get_rumor_detail(self.rumor_id)
        user = self.controller.current_user

        for k, v in rumor.items():
            tk.Label(self, text=f"{k}: {v}").pack(anchor="w")

        # ---------- verified ----------
        if rumor["status"] == "verified":
            result_text = (
                "ข้อมูลจริง" if rumor["verified_result"] == "true"
                else "ข้อมูลเท็จ"
            )
            tk.Label(
                self,
                text=f"ข่าวนี้ถูกยืนยันแล้ว: {result_text}",
                fg="green" if rumor["verified_result"] == "true" else "red"
            ).pack(pady=10)
            return

        # ---------- user ----------
        if user["role"] == "user":
            tk.Label(self, text="เลือกประเภทรายงาน").pack(anchor="w", pady=(10, 0))
            tk.Radiobutton(
                self,
                text="บิดเบือน",
                variable=self.report_type_var,
                value="บิดเบือน"
            ).pack(anchor="w")
            tk.Radiobutton(
                self,
                text="ปลุกปั่น",
                variable=self.report_type_var,
                value="ปลุกปั่น"
            ).pack(anchor="w")
            tk.Radiobutton(
                self,
                text="ข้อมูลเท็จ",
                variable=self.report_type_var,
                value="ข้อมูลเท็จ"
            ).pack(anchor="w")
            tk.Button(
                self,
                text="รายงานข่าว",
                command=self.report
            ).pack(pady=10)
        # ---------- checker ----------
        if user["role"] == "checker":
            tk.Label(self, text="ยืนยันข่าว:").pack(pady=5)

            tk.Button(
                self,
                text="ยืนยันว่าเป็นข้อมูลจริง",
                fg="green",
                command=lambda: self.verify("true")
            ).pack(pady=3)

            tk.Button(
                self,
                text="ยืนยันว่าเป็นข้อมูลเท็จ",
                fg="red",
                command=lambda: self.verify("false")
            ).pack(pady=3)

    def report(self):
        report_type = self.report_type_var.get() 
        result = self.controller.report_rumor(
            rumor_id=self.rumor_id,
            report_type= report_type 
        )
        messagebox.showinfo("ผลลัพธ์", result)
        self.refresh()

    def verify(self, result):
        msg = self.controller.verify_rumor(self.rumor_id, result)
        messagebox.showinfo("ผลลัพธ์", msg)
        self.refresh()

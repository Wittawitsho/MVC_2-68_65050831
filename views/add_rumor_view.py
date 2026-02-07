import tkinter as tk
from tkinter import messagebox

class AddRumorView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("แจ้งข่าวลือใหม่")

        tk.Label(self, text="หัวข้อข่าว").pack(anchor="w")
        self.title_entry = tk.Entry(self, width=40)
        self.title_entry.pack()

        tk.Label(self, text="แหล่งที่มา").pack(anchor="w", pady=(10, 0))
        self.source_entry = tk.Entry(self, width=40)
        self.source_entry.pack()

        tk.Button(
            self,
            text="บันทึกข่าวลือ",
            command=self.submit
        ).pack(pady=10)

    def submit(self):
        title = self.title_entry.get()
        source = self.source_entry.get()

        if not title or not source:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบ")
            return

        msg = self.controller.add_rumor(title, source)
        messagebox.showinfo("สำเร็จ", msg)
        self.destroy()

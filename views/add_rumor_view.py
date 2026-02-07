import tkinter as tk
from tkinter import messagebox

class AddRumorView(tk.Toplevel):
    def __init__(self, master, controller, on_success=None):
        super().__init__(master)
        self.controller = controller
        self.on_success = on_success
        self.title("แจ้งข่าวลือใหม่")
        self.geometry("400x250")

        tk.Label(self, text="หัวข้อข่าว", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(20, 5))
        self.title_entry = tk.Entry(self, width=40, font=("Arial", 10))
        self.title_entry.pack(padx=20)

        tk.Label(self, text="แหล่งที่มา", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 5))
        self.source_entry = tk.Entry(self, width=40, font=("Arial", 10))
        self.source_entry.pack(padx=20)

        tk.Button(
            self,
            text="บันทึกข่าวลือ",
            command=self.submit,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(pady=20)

    def submit(self):
        title = self.title_entry.get().strip()
        source = self.source_entry.get().strip()

        if not title or not source:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบ")
            return

        msg = self.controller.add_rumor(title, source)
        messagebox.showinfo("สำเร็จ", msg)
        
        if self.on_success:
            self.on_success()
        
        self.destroy()
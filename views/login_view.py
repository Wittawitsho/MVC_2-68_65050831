import tkinter as tk
from tkinter import messagebox


class LoginView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Login")
        self.geometry("300x200")

        tk.Label(self, text="User ID").pack(pady=5)
        self.entry = tk.Entry(self)
        self.entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=15)

    def login(self):
        user_id = self.entry.get()

        if self.controller.login(user_id):
            self.destroy()

            # ✅ import ตรงนี้แทน
            from views.main_window import MainWindow
            MainWindow(self.controller)

        else:
            messagebox.showerror("Error", "User ID ไม่ถูกต้อง")

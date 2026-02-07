import tkinter as tk
from views.add_rumor_view import AddRumorView
from views.rumor_list_view import RumorListView
from views.summary_view import SummaryView


class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Rumor Tracking System")
        self.geometry("400x300")

        user = controller.current_user
        tk.Label(self,
                 text=f"Welcome {user['name']}  (Role: {user['role']})"
                 ).pack(pady=5)
        tk.Button(
            self,
            text="+ แจ้งข่าวลือใหม่",
            command=lambda: AddRumorView(self, controller)
        ).pack(pady=5)
        tk.Button(
            self, text="หน้ารวมข่าวลือ",
            command=lambda: RumorListView(self, controller)
        ).pack(fill="x", padx=40, pady=5)

        tk.Button(
            self, text="หน้าสรุปผล",
            command=lambda: SummaryView(self, controller)
        ).pack(fill="x", padx=40, pady=5)

        tk.Button(
            self, text="Logout",
            fg="red",
            command=self.logout
        ).pack(pady=15)

        self.mainloop()

    def logout(self):
        self.controller.logout()
        self.destroy()

        # ✅ import ตอนใช้งาน
        from views.login_view import LoginView
        LoginView(self.controller)

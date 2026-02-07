import tkinter as tk
from views.add_rumor_view import AddRumorView
from views.rumor_list_view import RumorListView
from views.summary_view import SummaryView


class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Rumor Tracking System")
        self.geometry("450x400")
        
        self.active_windows = []

        user = controller.current_user
        
        # Header
        header_frame = tk.Frame(self, bg="#1976D2")
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text=f"Welcome {user['name']}",
            font=("Arial", 14, "bold"),
            bg="#1976D2",
            fg="white",
            pady=10
        ).pack()
        
        tk.Label(
            header_frame,
            text=f"Role: {user['role'].upper()}",
            font=("Arial", 10),
            bg="#1976D2",
            fg="white",
            pady=5
        ).pack()
        
        # Main Menu
        menu_frame = tk.Frame(self, bg="white")
        menu_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # ปุ่มเพิ่มข่าว
        tk.Button(
            menu_frame,
            text="+ แจ้งข่าวลือใหม่",
            command=self.open_add_rumor,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            cursor="hand2",
            height=2
        ).pack(fill="x", pady=10)
        
        # ปุ่มดูรายการข่าว
        tk.Button(
            menu_frame,
            text="หน้ารวมข่าวลือ",
            command=self.open_rumor_list,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            cursor="hand2",
            height=2
        ).pack(fill="x", pady=10)

        # ปุ่มสรุปผล
        tk.Button(
            menu_frame,
            text="หน้าสรุปผล",
            command=self.open_summary,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12),
            cursor="hand2",
            height=2
        ).pack(fill="x", pady=10)

        # ปุ่ม Logout
        tk.Button(
            menu_frame,
            text="Logout",
            fg="white",
            bg="#f44336",
            font=("Arial", 12),
            cursor="hand2",
            command=self.logout,
            height=2
        ).pack(fill="x", pady=10)

        self.mainloop()

    def open_add_rumor(self):
        AddRumorView(self, self.controller, on_success=self.refresh_all_windows)
    
    def open_rumor_list(self):
        window = RumorListView(self, self.controller)
        self.active_windows.append(window)
    
    def open_summary(self):
        window = SummaryView(self, self.controller)
        self.active_windows.append(window)
    
    def refresh_all_windows(self):
        for window in self.active_windows:
            try:
                if window.winfo_exists() and hasattr(window, 'refresh'):
                    window.refresh()
            except:
                pass

    def logout(self):
        self.controller.logout()
        self.destroy()

        from views.login_view import LoginView
        LoginView(self.controller)
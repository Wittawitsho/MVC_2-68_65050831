import tkinter as tk
from tkinter import messagebox


class RumorDetailView(tk.Toplevel):
    def __init__(self, master, controller, rumor_id, on_close=None):
        super().__init__(master)
        self.controller = controller
        self.rumor_id = rumor_id
        self.on_close = on_close
        self.title("รายละเอียดข่าวลือ")
        self.geometry("500x600")
        self.report_type_var = tk.StringVar(value="ข้อมูลเท็จ")
        
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        self.refresh()

    def on_window_close(self):
        if self.on_close:
            self.on_close()
        self.destroy()

    def refresh(self):
        # ลบ widget เก่าทั้งหมด
        for w in self.winfo_children():
            w.destroy()

        rumor = self.controller.get_rumor_detail(self.rumor_id)
        user = self.controller.current_user

        # Header
        header_frame = tk.Frame(self, bg="#2196F3")
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="รายละเอียดข่าวลือ",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            pady=10
        ).pack(padx=20)

        # Content Frame
        content_frame = tk.Frame(self, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # แสดงข้อมูลข่าว
        info_frame = tk.Frame(content_frame, bg="#f5f5f5", relief="solid", borderwidth=1)
        info_frame.pack(fill="x", pady=10)

        # Title
        tk.Label(
            info_frame,
            text=rumor.get("title", "ไม่ระบุหัวข้อ"),
            font=("Arial", 13, "bold"),
            bg="#f5f5f5",
            wraplength=400,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(15, 10))

        # รายละเอียด
        details = [
            ("รหัสข่าว", rumor.get("rumor_id", "-")),
            ("แหล่งที่มา", rumor.get("source", "-")),
            ("วันที่สร้าง", rumor.get("date_created") or rumor.get("date", "-")),
            ("คะแนนความน่าเชื่อถือ", rumor.get("credibility_score") or rumor.get("credibility", 0)),
            ("จำนวนรายงาน", rumor.get("report_count", 0)),
            ("สถานะ", rumor.get("status", "normal"))
        ]

        for label, value in details:
            row = tk.Frame(info_frame, bg="#f5f5f5")
            row.pack(fill="x", padx=15, pady=2)
            
            tk.Label(
                row,
                text=f"{label}:",
                font=("Arial", 10),
                bg="#f5f5f5",
                width=20,
                anchor="w"
            ).pack(side="left")
            
            # สีสำหรับสถานะ
            color = "black"
            if label == "สถานะ" and value == "panic":
                color = "red"
            
            tk.Label(
                row,
                text=str(value),
                font=("Arial", 10, "bold" if label == "สถานะ" else "normal"),
                bg="#f5f5f5",
                fg=color,
                anchor="w"
            ).pack(side="left", padx=10)

        # VERIFIED
        if rumor["status"] == "verified":
            result_text = (
                "✓ ยืนยันแล้ว: ข้อมูลจริง" if rumor["verified_result"] == "true"
                else "✗ ยืนยันแล้ว: ข้อมูลเท็จ"
            )
            result_color = "green" if rumor["verified_result"] == "true" else "red"
            result_bg = "#e8f5e9" if rumor["verified_result"] == "true" else "#ffebee"
            
            verified_frame = tk.Frame(content_frame, bg=result_bg, relief="solid", borderwidth=1)
            verified_frame.pack(fill="x", pady=15)
            
            tk.Label(
                verified_frame,
                text=result_text,
                font=("Arial", 12, "bold"),
                bg=result_bg,
                fg=result_color,
                pady=15
            ).pack()
            
            return  # ไม่แสดงปุ่มรายงาน/ยืนยัน

        # USER: รายงานข่าว
        if user["role"] == "user":
            action_frame = tk.Frame(content_frame, bg="white")
            action_frame.pack(fill="x", pady=15)
            
            tk.Label(
                action_frame,
                text="เลือกประเภทรายงาน:",
                font=("Arial", 11, "bold"),
                bg="white"
            ).pack(anchor="w", pady=(0, 10))
            
            for option in ["บิดเบือน", "ปลุกปั่น", "ข้อมูลเท็จ"]:
                tk.Radiobutton(
                    action_frame,
                    text=option,
                    variable=self.report_type_var,
                    value=option,
                    font=("Arial", 10),
                    bg="white"
                ).pack(anchor="w", padx=20)
            
            tk.Button(
                action_frame,
                text="รายงานข่าว",
                command=self.report,
                bg="#ff9800",
                fg="white",
                font=("Arial", 11, "bold"),
                cursor="hand2",
                width=20
            ).pack(pady=15)

        # CHECKER: ยืนยันข่าว
        elif user["role"] == "checker":
            action_frame = tk.Frame(content_frame, bg="white")
            action_frame.pack(fill="x", pady=15)
            
            tk.Label(
                action_frame,
                text="ยืนยันข่าวนี้:",
                font=("Arial", 11, "bold"),
                bg="white"
            ).pack(pady=(0, 10))

            button_frame = tk.Frame(action_frame, bg="white")
            button_frame.pack()

            tk.Button(
                button_frame,
                text="ยืนยันว่าเป็นข้อมูลจริง",
                fg="white",
                bg="#4CAF50",
                font=("Arial", 10, "bold"),
                cursor="hand2",
                width=25,
                command=lambda: self.verify("true")
            ).pack(side="left", padx=5, pady=5)

            tk.Button(
                button_frame,
                text="ยืนยันว่าเป็นข้อมูลเท็จ",
                fg="white",
                bg="#f44336",
                font=("Arial", 10, "bold"),
                cursor="hand2",
                width=25,
                command=lambda: self.verify("false")
            ).pack(side="left", padx=5, pady=5)

    def report(self):
        report_type = self.report_type_var.get()
        result = self.controller.report_rumor(
            rumor_id=self.rumor_id,
            report_type=report_type
        )
        messagebox.showinfo("ผลลัพธ์", result)
        self.refresh()
        if self.on_close:
            self.on_close()

    def verify(self, result):
        confirm = messagebox.askyesno(
            "ยืนยัน",
            f"คุณแน่ใจหรือไม่ที่จะยืนยันข่าวนี้เป็น {'ข้อมูลจริง' if result == 'true' else 'ข้อมูลเท็จ'}?"
        )
        
        if not confirm:
            return
        
        msg = self.controller.verify_rumor(self.rumor_id, result)
        messagebox.showinfo("ผลลัพธ์", msg)
        self.refresh()
        if self.on_close:
            self.on_close()
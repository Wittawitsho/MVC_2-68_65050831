import tkinter as tk
from tkinter import ttk
from views.rumor_detail_view import RumorDetailView


class RumorListView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("รวมข่าวลือ")
        self.geometry("700x500")
        
        # Header
        header_frame = tk.Frame(self, bg="#2196F3")
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="รายการข่าวลือทั้งหมด (เรียงตามจำนวนรายงาน)",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            pady=15
        ).pack(padx=20)
        
        # Scrollable Frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ✅ Auto-refresh เมื่อหน้าต่างได้รับ focus
        self.bind("<FocusIn>", lambda e: self.refresh())
        
        # ✅ โหลดข้อมูลครั้งแรก
        self.refresh()
    
    def refresh(self):
        # ลบข้อมูลเก่า
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # โหลดข้อมูลใหม่
        rumors = self.controller.get_rumors()
        rumors.sort(key=lambda x: x["report_count"], reverse=True)
        
        if not rumors:
            tk.Label(
                self.scrollable_frame,
                text="ไม่มีข่าวลือในระบบ",
                font=("Arial", 12),
                fg="gray"
            ).pack(pady=20)
            return
        
        for r in rumors:
            # สร้างกรอบสำหรับแต่ละข่าว
            frame = tk.Frame(self.scrollable_frame, relief="solid", borderwidth=1, bg="white")
            frame.pack(fill="x", padx=5, pady=5)
            
            # ข้อมูลข่าว
            info_frame = tk.Frame(frame, bg="white")
            info_frame.pack(fill="x", padx=10, pady=10)
            
            # หัวข้อ
            tk.Label(
                info_frame,
                text=r["title"],
                font=("Arial", 11, "bold"),
                bg="white",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
            
            # สถานะและจำนวนรายงาน
            status_text = f'รายงาน: {r["report_count"]}'
            status_color = "black"
            
            if r["status"] == "panic":
                status_text += " (PANIC)"
                status_color = "red"
            elif r["status"] == "verified":
                result = "✓ จริง" if r.get("verified_result") == "true" else "✗ เท็จ"
                status_text += f" (ยืนยันแล้ว: {result})"
                status_color = "green" if r.get("verified_result") == "true" else "orange"
            
            tk.Label(
                info_frame,
                text=status_text,
                font=("Arial", 9),
                fg=status_color,
                bg="white"
            ).pack(side="right", padx=10)
            
            # ปุ่มดูรายละเอียด
            btn = tk.Button(
                frame,
                text="ดูรายละเอียด",
                command=lambda rid=r["rumor_id"]: self.open_detail(rid),
                bg="#2196F3",
                fg="white",
                cursor="hand2",
                font=("Arial", 9)
            )
            btn.pack(side="right", padx=10, pady=(0, 10))
    
    def open_detail(self, rumor_id):
        detail_window = RumorDetailView(self, self.controller, rumor_id, on_close=self.refresh)
import tkinter as tk
from tkinter import ttk


class SummaryView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("สรุปผล")
        self.geometry("700x600")
        
        # Header
        header_frame = tk.Frame(self, bg="#2196F3")
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="สรุปผลข่าวลือ",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            pady=15
        ).pack(padx=20)
        
        # Content Frame with Scrollbar
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Auto-refresh เมื่อหน้าต่างได้รับ focus
        self.bind("<FocusIn>", lambda e: self.refresh())
        
        # โหลดข้อมูลครั้งแรก
        self.refresh()
    
    def refresh(self):
        # ลบข้อมูลเก่า
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        rumors = self.controller.get_rumors()

        # PANIC
        panic_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="ข่าวลือสถานะ PANIC",
            font=("Arial", 12, "bold"),
            fg="red",
            bg="white",
            padx=15,
            pady=10
        )
        panic_frame.pack(fill="x", padx=10, pady=10)
        
        panic_rumors = [r for r in rumors if r["status"] == "panic"]
        
        if not panic_rumors:
            tk.Label(
                panic_frame,
                text="ไม่มีข่าวลือในสถานะ panic",
                font=("Arial", 10),
                fg="gray",
                bg="white"
            ).pack(anchor="w")
        else:
            for r in panic_rumors:
                item_frame = tk.Frame(panic_frame, bg="#ffebee", relief="solid", borderwidth=1)
                item_frame.pack(fill="x", pady=3)
                
                tk.Label(
                    item_frame,
                    text=f"• {r['title']} (รายงาน: {r['report_count']})",
                    font=("Arial", 10),
                    bg="#ffebee",
                    anchor="w",
                    padx=10,
                    pady=5
                ).pack(fill="x")

        # VERIFIED TRUE
        true_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="ข่าวที่ยืนยันว่าเป็นข้อมูลจริง",
            font=("Arial", 12, "bold"),
            fg="green",
            bg="white",
            padx=15,
            pady=10
        )
        true_frame.pack(fill="x", padx=10, pady=10)
        
        true_rumors = [
            r for r in rumors 
            if r["status"] == "verified" and r["verified_result"] == "true"
        ]
        
        if not true_rumors:
            tk.Label(
                true_frame,
                text="ไม่มีข่าวที่ยืนยันว่าเป็นข้อมูลจริง",
                font=("Arial", 10),
                fg="gray",
                bg="white"
            ).pack(anchor="w")
        else:
            for r in true_rumors:
                item_frame = tk.Frame(true_frame, bg="#e8f5e9", relief="solid", borderwidth=1)
                item_frame.pack(fill="x", pady=3)
                
                tk.Label(
                    item_frame,
                    text=f"✓ {r['title']}",
                    font=("Arial", 10),
                    bg="#e8f5e9",
                    fg="green",
                    anchor="w",
                    padx=10,
                    pady=5
                ).pack(fill="x")

        # VERIFIED FALSE
        false_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="ข่าวที่ยืนยันว่าเป็นข้อมูลเท็จ",
            font=("Arial", 12, "bold"),
            fg="red",
            bg="white",
            padx=15,
            pady=10
        )
        false_frame.pack(fill="x", padx=10, pady=10)
        
        false_rumors = [
            r for r in rumors 
            if r["status"] == "verified" and r["verified_result"] == "false"
        ]
        
        if not false_rumors:
            tk.Label(
                false_frame,
                text="ไม่มีข่าวที่ยืนยันว่าเป็นข้อมูลเท็จ",
                font=("Arial", 10),
                fg="gray",
                bg="white"
            ).pack(anchor="w")
        else:
            for r in false_rumors:
                item_frame = tk.Frame(false_frame, bg="#fff3e0", relief="solid", borderwidth=1)
                item_frame.pack(fill="x", pady=3)
                
                tk.Label(
                    item_frame,
                    text=f"✗ {r['title']}",
                    font=("Arial", 10),
                    bg="#fff3e0",
                    fg="red",
                    anchor="w",
                    padx=10,
                    pady=5
                ).pack(fill="x")
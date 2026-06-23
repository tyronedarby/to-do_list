import tkinter as tk
from tkinter import messagebox, font


class BeautifulTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimalist To-Do")
        self.root.geometry("420x550")
        self.root.configure(bg="#F4F6F9")  # Soft light grey background
        self.root.resizable(False, False)

        # Force the window to the front on macOS
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_call = self.root.after(1, lambda: self.root.attributes("-topmost", False))

        # Define custom clean fonts
        self.title_font = font.Font(family="Helvetica", size=26, weight="bold")
        self.task_font = font.Font(family="Helvetica", size=12)
        self.btn_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Color Palette
        self.BG_COLOR = "#F4F6F9"
        self.CARD_COLOR = "#FFFFFF"
        self.TEXT_COLOR = "#2D3748"
        self.ACCENT_COLOR = "#4A90E2"  # Vibrant blue for Add button
        self.DELETE_COLOR = "#FF6B6B"  # Soft red for delete

        # --- Title ---
        self.title_label = tk.Label(
            root, text="My Tasks", font=self.title_font,
            fg=self.TEXT_COLOR, bg=self.BG_COLOR
        )
        self.title_label.pack(anchor="w", padx=25, pady=(30, 20))

        # --- Input Section ---
        self.input_frame = tk.Frame(root, bg=self.BG_COLOR)
        self.input_frame.pack(fill="x", padx=25, pady=(0, 20))

        self.entry_var = tk.StringVar()
        self.task_entry = tk.Entry(
            self.input_frame, textvariable=self.entry_var, font=self.task_font,
            bg=self.CARD_COLOR, fg=self.TEXT_COLOR, relief="flat",
            insertbackground=self.TEXT_COLOR, highlightthickness=1,
            highlightbackground="#E2E8F0", highlightcolor=self.ACCENT_COLOR
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = tk.Button(
            self.input_frame, text="Add Task", font=self.btn_font,
            bg=self.ACCENT_COLOR, fg="#FFFFFF", relief="flat",
            activebackground="#357ABD", activeforeground="#FFFFFF",
            cursor="hand2", command=self.add_task, padx=15
        )
        self.add_button.pack(side="right", ipady=6)

        # --- Scrollable Task Container ---
        self.container = tk.Frame(root, bg=self.BG_COLOR)
        self.container.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        self.canvas = tk.Canvas(self.container, bg=self.BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=self.BG_COLOR)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Adjusted width dynamically to fit standard Mac screen scaling
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=360)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.task_rows = []

    def add_task(self):
        task_text = self.entry_var.get().strip()
        if not task_text:
            messagebox.showwarning("Empty Task", "Please enter a task description!")
            return

        row_frame = tk.Frame(self.scrollable_frame, bg=self.CARD_COLOR, highlightthickness=1,
                             highlightbackground="#E2E8F0")
        row_frame.pack(fill="x", pady=5, ipady=6)

        lbl = tk.Label(
            row_frame, text=task_text, font=self.task_font,
            fg=self.TEXT_COLOR, bg=self.CARD_COLOR, anchor="w"
        )
        lbl.pack(side="left", padx=15, fill="x", expand=True)

        del_btn = tk.Button(
            row_frame, text="✕", font=("Helvetica", 10, "bold"),
            bg=self.CARD_COLOR, fg=self.DELETE_COLOR, relief="flat",
            activebackground="#FFF5F5", activeforeground=self.DELETE_COLOR,
            cursor="hand2", command=lambda: self.remove_task(row_frame)
        )
        del_btn.pack(side="right", padx=10)

        self.entry_var.set("")
        self.task_rows.append(row_frame)
        self.canvas.yview_moveto(1.0)

    def remove_task(self, row_frame):
        row_frame.destroy()
        self.task_rows.remove(row_frame)


# CRITICAL: These lines must be at the very bottom of the file to launch it!
if __name__ == "__main__":
    root = tk.Tk()
    app = BeautifulTodoApp(root)
    root.mainloop()  # Keeps the window open
import tkinter as tk
from tkinter import messagebox
import os
import csv

BG        = "#07111F"
PANEL     = "#0F1A30"
CARD      = "#16233A"
TITLE     = "#00D4FF"
TEXT      = "#F8FAFC"
SECONDARY = "#94A3B8"
SUCCESS   = "#22C55E"
DANGER    = "#EF4444"
INPUT_BG  = "#0D1B2E"

HISTORY_FILE = "chat_history.csv"


class History:

    def __init__(self, username, client=None):

        self.username = username
        self.all_rows = []

        self.root = tk.Toplevel()
        self.root.title("SentinelChat — Chat History")
        self.root.geometry("860x640")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._build()
        self._load()

    def _build(self):

        # Top bar
        top = tk.Frame(self.root, bg=PANEL, height=60)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="📜  CHAT HISTORY", font=("Segoe UI", 16, "bold"),
                 fg=TITLE, bg=PANEL).pack(side="left", padx=25, pady=15)
        tk.Label(top, text=f"👤 {self.username}", font=("Segoe UI", 10),
                 fg=SECONDARY, bg=PANEL).pack(side="right", padx=25)

        # Search bar
        search_row = tk.Frame(self.root, bg=BG, pady=14)
        search_row.pack(fill="x", padx=25)

        tk.Label(search_row, text="⌕", font=("Segoe UI", 14),
                 fg=SECONDARY, bg=BG).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._filter())

        search_entry = tk.Entry(
            search_row, textvariable=self.search_var,
            font=("Segoe UI", 11), bg=INPUT_BG, fg=TEXT,
            insertbackground=TITLE, relief="flat"
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=7)
        search_entry.insert(0, "Search messages, users...")

        def clear_hint(e):
            if search_entry.get() == "Search messages, users...":
                search_entry.delete(0, "end")

        search_entry.bind("<FocusIn>", clear_hint)

        # Filter buttons
        filter_row = tk.Frame(self.root, bg=BG)
        filter_row.pack(fill="x", padx=25, pady=(0, 10))

        self.filter_var = tk.StringVar(value="ALL")

        for label, val in [("All", "ALL"), ("Private", "PRIVATE"),
                            ("Broadcast", "BROADCAST"), ("Group", "GROUP")]:
            rb = tk.Radiobutton(
                filter_row, text=label, variable=self.filter_var, value=val,
                command=self._filter,
                bg=BG, fg=SECONDARY, activebackground=BG,
                selectcolor=BG, activeforeground=TITLE,
                font=("Segoe UI", 10)
            )
            rb.pack(side="left", padx=(0, 14))

        # Log display
        log_frame = tk.Frame(self.root, bg=BG)
        log_frame.pack(fill="both", expand=True, padx=25, pady=(0, 10))

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log_display = tk.Text(
            log_frame, font=("Courier New", 10),
            bg=INPUT_BG, fg=TEXT, relief="flat",
            state="disabled", wrap="word",
            padx=12, pady=10, spacing1=3,
            yscrollcommand=scrollbar.set
        )
        self.log_display.pack(fill="both", expand=True)
        scrollbar.config(command=self.log_display.yview)

        self.log_display.tag_config("timestamp", foreground=SECONDARY)
        self.log_display.tag_config("sender", foreground=TITLE)
        self.log_display.tag_config("private", foreground="#8B5CF6")
        self.log_display.tag_config("broadcast", foreground=SUCCESS)
        self.log_display.tag_config("group", foreground="#F59E0B")
        self.log_display.tag_config("normal", foreground=TEXT)
        self.log_display.tag_config("header", foreground=TITLE)

        # Status row
        bottom = tk.Frame(self.root, bg=PANEL, height=40)
        bottom.pack(side="bottom", fill="x")
        bottom.pack_propagate(False)

        self.count_label = tk.Label(
            bottom, text="", font=("Segoe UI", 9),
            fg=SECONDARY, bg=PANEL
        )
        self.count_label.pack(side="left", padx=20, pady=10)

        tk.Button(
            bottom, text="Export CSV", bg=CARD, fg=SECONDARY,
            relief="flat", cursor="hand2", font=("Segoe UI", 9),
            command=self._export
        ).pack(side="right", padx=20, pady=6)

    def _load(self):
        self.all_rows = []

        if not os.path.exists(HISTORY_FILE):
            self._append_display("header",
                "No chat_history.csv found.\nStart chatting to generate history.\n")
            return

        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(
                    line for line in f if line.strip()
                )
                for row in reader:
                    clean = {}
                    for k, v in row.items():
                        if isinstance(v, list):
                            clean[k] = " ".join(map(str, v))
                        else:
                            clean[k] = "" if v is None else str(v)
                    self.all_rows.append(clean)
        except Exception as e:
            self._append_display("header", f"Error reading history: {e}\n")
            return

        self._filter()

    def _filter(self):
        query = self.search_var.get().lower().strip()
        if query == "search messages, users...":
            query = ""

        ftype = self.filter_var.get()

        filtered = []
        for row in self.all_rows:
            mtype = row.get("message_type", "")
            if ftype != "ALL" and ftype not in mtype:
                continue
            combined = " ".join(
    " ".join(v) if isinstance(v, list) else str(v)
    for v in row.values()
).lower()
            if query and query not in combined:
                continue
            filtered.append(row)

        self._render(filtered)

    def _render(self, rows):
        self.log_display.config(state="normal")
        self.log_display.delete("1.0", "end")

        if not rows:
            self.log_display.insert("end", "No messages match your filter.\n", "header")
        else:
            for row in rows:
                ts = row.get("timestamp", "")
                sender = row.get("sender", "")
                receiver = row.get("receiver", "")
                mtype = row.get("message_type", "")
                msg = row.get("message", "")

                tag = "normal"
                if "PRIVATE" in mtype:
                    tag = "private"
                elif "BROADCAST" in mtype:
                    tag = "broadcast"
                elif "GROUP" in mtype:
                    tag = "group"

                self.log_display.insert("end", f"[{ts}] ", "timestamp")
                self.log_display.insert("end", f"{sender}", "sender")
                self.log_display.insert("end", f" → {receiver} ", "timestamp")
                self.log_display.insert("end", f"[{mtype}]  ", tag)
                self.log_display.insert("end", f"{msg}\n", "normal")

        self.log_display.config(state="disabled")
        self.count_label.config(text=f"Showing {len(rows)} message(s)")

    def _append_display(self, tag, text):
        self.log_display.config(state="normal")
        self.log_display.insert("end", text, tag)
        self.log_display.config(state="disabled")

    def _export(self):
        try:
            import shutil
            dest = "chat_history_export.csv"
            shutil.copy(HISTORY_FILE, dest)
            messagebox.showinfo("Exported", f"Saved as {dest}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))


if __name__ == "__main__":
    History("MUSKAN")
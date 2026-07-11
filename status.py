import tkinter as tk
import time
import os
import csv
import random

BG        = "#07111F"
PANEL     = "#0F1A30"
CARD      = "#16233A"
CARD2     = "#1A2940"
TITLE     = "#00D4FF"
PURPLE    = "#8B5CF6"
TEXT      = "#F8FAFC"
SECONDARY = "#94A3B8"
SUCCESS   = "#22C55E"
DANGER    = "#EF4444"
WARNING   = "#F59E0B"

HISTORY_FILE = "chat_history.csv"


class Status:

    def __init__(self, username, client=None):

        self.username = username
        self.client = client
        self._running = True

        self.root = tk.Toplevel()
        self.root.title("SentinelChat — Server Status")
        self.root.geometry("860x660")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build()
        self._refresh_loop()

    def _build(self):

        # Top bar
        top = tk.Frame(self.root, bg=PANEL, height=60)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="🖥  SERVER ANALYTICS", font=("Segoe UI", 16, "bold"),
                 fg=TITLE, bg=PANEL).pack(side="left", padx=25, pady=15)

        self.live_dot = tk.Label(top, text="🟢 LIVE", font=("Segoe UI", 10, "bold"),
                                  fg=SUCCESS, bg=PANEL)
        self.live_dot.pack(side="right", padx=25)

        # Stats cards row
        stats_row = tk.Frame(self.root, bg=BG)
        stats_row.pack(fill="x", padx=25, pady=20)

        self.stat_frames = {}
        stats = [
            ("👥", "Connected Users", "users", TITLE),
            ("💬", "Total Messages", "msgs", PURPLE),
            ("📡", "Broadcasts", "broadcasts", SUCCESS),
            ("🔐", "Private Msgs", "private", WARNING),
        ]

        for icon, label, key, color in stats:
            f = tk.Frame(stats_row, bg=CARD, width=180, height=110)
            f.pack_propagate(False)
            f.pack(side="left", padx=8, expand=True, fill="x")

            tk.Label(f, text=icon, font=("Segoe UI", 20), bg=CARD, fg=color).pack(pady=(12, 2))

            val_lbl = tk.Label(f, text="—", font=("Segoe UI", 18, "bold"), bg=CARD, fg=color)
            val_lbl.pack()

            tk.Label(f, text=label, font=("Segoe UI", 9), bg=CARD, fg=SECONDARY).pack()

            self.stat_frames[key] = val_lbl

        # Network bar
        net_frame = tk.Frame(self.root, bg=CARD, padx=20, pady=14)
        net_frame.pack(fill="x", padx=25)

        tk.Label(net_frame, text="NETWORK THROUGHPUT", font=("Segoe UI", 9, "bold"),
                 fg=SECONDARY, bg=CARD).pack(anchor="w")

        bar_row = tk.Frame(net_frame, bg=CARD)
        bar_row.pack(fill="x", pady=(8, 0))

        tk.Label(bar_row, text="CPU", font=("Segoe UI", 9), fg=SECONDARY, bg=CARD, width=8).pack(side="left")
        self.cpu_bar = tk.Canvas(bar_row, height=14, bg=PANEL, relief="flat",
                                  highlightthickness=0)
        self.cpu_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.cpu_pct = tk.Label(bar_row, text="", font=("Segoe UI", 9), fg=TITLE, bg=CARD, width=5)
        self.cpu_pct.pack(side="left")

        bar_row2 = tk.Frame(net_frame, bg=CARD)
        bar_row2.pack(fill="x", pady=(6, 0))

        tk.Label(bar_row2, text="MEM", font=("Segoe UI", 9), fg=SECONDARY, bg=CARD, width=8).pack(side="left")
        self.mem_bar = tk.Canvas(bar_row2, height=14, bg=PANEL, relief="flat",
                                  highlightthickness=0)
        self.mem_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.mem_pct = tk.Label(bar_row2, text="", font=("Segoe UI", 9), fg=PURPLE, bg=CARD, width=5)
        self.mem_pct.pack(side="left")

        # Log viewer
        tk.Label(self.root, text="RECENT ACTIVITY LOG", font=("Segoe UI", 9, "bold"),
                 fg=SECONDARY, bg=BG).pack(anchor="w", padx=25, pady=(18, 4))

        log_frame = tk.Frame(self.root, bg=BG)
        log_frame.pack(fill="both", expand=True, padx=25, pady=(0, 10))

        sb = tk.Scrollbar(log_frame)
        sb.pack(side="right", fill="y")

        self.log_text = tk.Text(
            log_frame, font=("Courier New", 10), bg="#0D1B2E", fg=TEXT,
            relief="flat", state="disabled", wrap="word",
            padx=10, pady=8, spacing1=3,
            yscrollcommand=sb.set
        )
        self.log_text.pack(fill="both", expand=True)
        sb.config(command=self.log_text.yview)

        self.log_text.tag_config("ts", foreground=SECONDARY)
        self.log_text.tag_config("type", foreground=TITLE)
        self.log_text.tag_config("msg", foreground=TEXT)

        # Footer
        footer = tk.Frame(self.root, bg=PANEL, height=40)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)

        self.last_updated = tk.Label(
            footer, text="", font=("Segoe UI", 9),
            fg=SECONDARY, bg=PANEL
        )
        self.last_updated.pack(side="left", padx=20, pady=10)

        tk.Label(footer, text="ISEA Summer Internship 2026",
                 font=("Segoe UI", 8), fg=SECONDARY, bg=PANEL).pack(side="right", padx=20)

    def _draw_bar(self, canvas, pct, color):
        canvas.update_idletasks()
        w = canvas.winfo_width()
        if w < 2:
            return
        canvas.delete("all")
        # Background
        canvas.create_rectangle(0, 0, w, 14, fill=PANEL, outline="")
        # Filled portion
        filled = int(w * pct / 100)
        canvas.create_rectangle(0, 0, filled, 14, fill=color, outline="")

    def _refresh_loop(self):
        if not self._running:
            return
        self._refresh()
        self.root.after(3000, self._refresh_loop)

    def _refresh(self):
        # Stats from CSV
        total = private = broadcast = group = 0

        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        total += 1
                        mtype = row.get("message_type", "")
                        if "PRIVATE" in mtype:
                            private += 1
                        elif "BROADCAST" in mtype:
                            broadcast += 1
            except Exception:
                pass

        self.stat_frames["users"].config(text=str(random.randint(1, 6)))
        self.stat_frames["msgs"].config(text=str(total))
        self.stat_frames["broadcasts"].config(text=str(broadcast))
        self.stat_frames["private"].config(text=str(private))

        # Bars — simulate live values
        cpu = random.randint(12, 72)
        mem = random.randint(30, 65)

        self.cpu_pct.config(text=f"{cpu}%")
        self.mem_pct.config(text=f"{mem}%")

        self.root.after(50, lambda: self._draw_bar(self.cpu_bar, cpu, TITLE))
        self.root.after(50, lambda: self._draw_bar(self.mem_bar, mem, PURPLE))

        # Log tail
        self._refresh_log()

        ts = time.strftime("%H:%M:%S")
        self.last_updated.config(text=f"Last updated: {ts}")

        # Heartbeat dot
        self.live_dot.config(text="🟢 LIVE" if int(time.time()) % 2 == 0 else "⚫ LIVE")

    def _refresh_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")

        if not os.path.exists(HISTORY_FILE):
            self.log_text.insert("end", "No activity yet.\n", "msg")
            self.log_text.config(state="disabled")
            return

        rows = []
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception:
            pass

        for row in rows[-20:]:
            ts = row.get("timestamp", "")
            sender = row.get("sender", "")
            mtype = row.get("message_type", "")
            msg = row.get("message", "")
            self.log_text.insert("end", f"[{ts}] ", "ts")
            self.log_text.insert("end", f"[{mtype}] ", "type")
            self.log_text.insert("end", f"{sender}: {msg}\n", "msg")

        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _on_close(self):
        self._running = False
        self.root.destroy()


if __name__ == "__main__":
    Status("MUSKAN")
import tkinter as tk
from tkinter import messagebox

BG       = "#07091A"
PANEL    = "#0D1333"
CARD     = "#111B3A"
GLOW     = "#00D4FF"
TEXT     = "#F0F4FF"
MUTED    = "#4A5580"
SUCCESS  = "#22C55E"
INPUT_BG = "#080F28"


class Broadcast:
    def __init__(self, username, client=None):
        self.username = username
        self.client   = client

        self.root = tk.Toplevel()
        self.root.title("SentinelChat — Broadcast")
        self.root.geometry("660x520")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._build()

    def _build(self):
        # Glow bar
        tk.Frame(self.root, bg=GLOW, height=2).pack(fill="x")

        # Top bar
        top = tk.Frame(self.root, bg=PANEL, height=54)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="📡  BROADCAST CENTER",
                 font=("Segoe UI", 14, "bold"), fg=GLOW, bg=PANEL).pack(side="left", padx=20, pady=14)
        tk.Label(top, text=f"👤 {self.username}",
                 font=("Segoe UI", 10), fg=MUTED, bg=PANEL).pack(side="right", padx=20)

        # Footer (anchor bottom first)
        tk.Frame(self.root, bg=PANEL, height=28).pack(side="bottom", fill="x")

        # Send button (above footer)
        self.send_btn = tk.Button(self.root,
            text="📡  SEND BROADCAST",
            font=("Segoe UI", 12, "bold"),
            bg=GLOW, fg="#000000",
            activebackground="#42E5FF", activeforeground="#000000",
            relief="flat", cursor="hand2", pady=13,
            command=self._send)
        self.send_btn.pack(side="bottom", fill="x", padx=30, pady=12)
        self.send_btn.bind("<Enter>", lambda e: self.send_btn.config(bg="#42E5FF"))
        self.send_btn.bind("<Leave>", lambda e: self.send_btn.config(bg=GLOW))

        # Status label
        self.status = tk.Label(self.root, text="",
                                font=("Segoe UI", 10, "bold"), fg=SUCCESS, bg=BG)
        self.status.pack(side="bottom", pady=(0, 2))

        # Counter
        self.counter = tk.Label(self.root, text="0 / 500 characters",
                                 font=("Segoe UI", 9), fg=MUTED, bg=BG)
        self.counter.pack(side="bottom", anchor="e", padx=30)

        # Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=30, pady=16)

        # Recipients badge
        tk.Label(body, text="RECIPIENTS",
                 font=("Segoe UI", 8, "bold"), fg=MUTED, bg=BG).pack(anchor="w")

        badge = tk.Frame(body, bg=CARD, padx=14, pady=8,
                          highlightthickness=1, highlightbackground=GLOW)
        badge.pack(anchor="w", pady=(4, 16))
        tk.Label(badge, text="📡  ALL CONNECTED USERS",
                 font=("Segoe UI", 10, "bold"), fg=GLOW, bg=CARD).pack()

        # Message box
        tk.Label(body, text="MESSAGE",
                 font=("Segoe UI", 8, "bold"), fg=MUTED, bg=BG).pack(anchor="w")

        border = tk.Frame(body, bg=GLOW, padx=1, pady=1)
        border.pack(fill="both", expand=True, pady=(4, 0))

        self.msg_box = tk.Text(border,
            font=("Segoe UI", 11), bg=INPUT_BG, fg=TEXT,
            insertbackground=GLOW, relief="flat", wrap="word",
            padx=12, pady=10)
        self.msg_box.pack(fill="both", expand=True)
        self.msg_box.bind("<KeyRelease>", self._count)

    def _count(self, e=None):
        n = len(self.msg_box.get("1.0", "end-1c"))
        self.counter.config(text=f"{n} / 500 characters",
                             fg="#EF4444" if n > 500 else MUTED)

    def _send(self):
        msg = self.msg_box.get("1.0", "end-1c").strip()
        if not msg:
            messagebox.showwarning("Empty", "Type a message first.")
            return
        if len(msg) > 500:
            messagebox.showerror("Too long", "Max 500 characters.")
            return
        try:
            if self.client:
                self.client.send(f"/all {msg}".encode())
            self.status.config(text="✅  Broadcast sent!")
            self.msg_box.delete("1.0", "end")
            self._count()
            self.root.after(3000, lambda: self.status.config(text=""))
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    Broadcast("MUSKAN")
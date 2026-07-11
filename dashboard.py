import tkinter as tk
from tkinter import messagebox
import time
import math

# ── TRUE CYBER PALETTE ────────────────────────────────────────
BG       = "#050510"   # true black-blue
PANEL    = "#0A0A1F"   # near-black panel
CARD     = "#0D0D24"   # card base
CARD_H   = "#141432"   # card hover
GLOW     = "#00D4FF"   # cyan
PURPLE   = "#8B5CF6"   # purple
PINK     = "#EC4899"   # accent pink
TEXT     = "#E8F0FF"   # near-white
MUTED    = "#3A4060"   # dimmed text
SUCCESS  = "#22C55E"
DANGER   = "#EF4444"


class Dashboard:
    def __init__(self, username, client=None):
        self.username = username
        self.client   = client
        self._tick_on = True
        self._after_ids = []

        self.root = tk.Tk()
        self.root.title("SentinelChat — Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG)
        from cyber_bg import CyberBackground

        CyberBackground(self.root)
        self.root.resizable(True, True)
        self.root.minsize(800, 560)

        self._build()
        self._clock_tick()
        self._heartbeat()

        self.root.protocol("WM_DELETE_WINDOW", self._exit)
        self.root.mainloop()

    # ─────────────────────────────────────────────────────────
    def _build(self):

        # ── Gradient top bar (3 stacked thin frames) ─────────
        for color, h in [(PURPLE, 1), (GLOW, 2), (PURPLE, 1)]:
            tk.Frame(self.root, bg=color, height=h).pack(fill="x")

        # ── Top navigation bar ────────────────────────────────
        top = tk.Frame(self.root, bg=PANEL, height=64)
        top.pack(fill="x")
        top.pack_propagate(False)

        # Left: logo
        left = tk.Frame(top, bg=PANEL)
        left.pack(side="left", padx=24, pady=10)

        logo_row = tk.Frame(left, bg=PANEL)
        logo_row.pack(anchor="w")

        tk.Label(logo_row, text="◈",
                 font=("Segoe UI", 18, "bold"), fg=GLOW, bg=PANEL).pack(side="left")
        tk.Label(logo_row, text="  SENTINEL CHAT",
                 font=("Segoe UI", 16, "bold"), fg=TEXT, bg=PANEL).pack(side="left")

        tk.Label(left, text="Secure Multi-Client TCP Communication",
                 font=("Segoe UI", 8), fg=MUTED, bg=PANEL).pack(anchor="w")

        # Right: status + clock
        right = tk.Frame(top, bg=PANEL)
        right.pack(side="right", padx=24, pady=10)

        hb_row = tk.Frame(right, bg=PANEL)
        hb_row.pack(anchor="e")
        self.hb_dot = tk.Label(hb_row, text="●",
                                font=("Segoe UI", 10), fg=SUCCESS, bg=PANEL)
        self.hb_dot.pack(side="left")
        tk.Label(hb_row, text="  SECURE  ·  ENCRYPTED",
                 font=("Segoe UI", 9, "bold"), fg=SUCCESS, bg=PANEL).pack(side="left")

        self.clock = tk.Label(right, text="",
                               font=("Segoe UI Mono", 11, "bold"), fg=GLOW, bg=PANEL)
        self.clock.pack(anchor="e", pady=(4, 0))

        # ── Thin separator ────────────────────────────────────
        tk.Frame(self.root, bg=MUTED, height=1).pack(fill="x", padx=20)

        # ── Welcome banner ────────────────────────────────────
        banner = tk.Frame(self.root, bg=BG)
        banner.pack(fill="x", padx=30, pady=(20, 4))

        tk.Label(banner,
                 text=f"WELCOME BACK,  {self.username.upper()}",
                 font=("Segoe UI", 20, "bold"), fg=GLOW, bg=BG).pack(anchor="w")
        tk.Label(banner,
                 text="All systems operational   ·   Network secure   ·   Port 5000",
                 font=("Segoe UI", 9), fg=MUTED, bg=BG).pack(anchor="w", pady=(3, 0))

        # ================= HERO PANEL =================

        hero_outer = tk.Frame(
            self.root,
            bg=PURPLE,
            padx=1,
            pady=1
        )
        hero_outer.pack(fill="x", padx=30, pady=(15,20))

        hero = tk.Frame(hero_outer, bg=CARD)
        hero.pack(fill="x")

        left = tk.Frame(hero, bg=CARD)
        left.pack(side="left", padx=22, pady=18)

        tk.Label(
            left,
            text="◈ CYBER OPERATIONS CENTER",
            font=("Segoe UI",18,"bold"),
            fg=GLOW,
            bg=CARD
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Secure Multi-Client TCP Platform",
            font=("Segoe UI",10),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", pady=(5,0))

        tk.Label(
            left,
            text="● TCP ACTIVE   ● SERVER ONLINE   ● ENCRYPTION ENABLED",
            font=("Segoe UI",9,"bold"),
            fg=SUCCESS,
            bg=CARD
        ).pack(anchor="w", pady=(10,0))

        stats = tk.Frame(hero,bg=CARD)
        stats.pack(side="right", padx=20)

        for value,title,color in [
            ("06","MODULES",GLOW),
            ("100%","SECURE",SUCCESS),
            ("5000","PORT",PURPLE),
        ]:

            box=tk.Frame(
                stats,
                bg="#1B2B45",
                padx=14,
                pady=10
            )
            box.pack(side="left", padx=6)

            tk.Label(
                box,
                text=value,
                font=("Segoe UI",18,"bold"),
                fg=color,
                bg="#1B2B45"
            ).pack()

            tk.Label(
                box,
                text=title,
                font=("Segoe UI",8),
                fg=MUTED,
                bg="#1B2B45"
            ).pack()

        # ── Card grid ─────────────────────────────────────────
        grid = tk.Frame(self.root, bg=BG)
        grid.pack(padx=24, pady=(12, 4), fill="both", expand=True)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        CARDS = [
            ("BROADCAST",     "Send announcements to all\nconnected users instantly",   GLOW,   self._open_broadcast, 0, 0),
            ("PRIVATE CHAT",  "Encrypted one-to-one\ndirect messaging",                 PURPLE, self._open_private,   0, 1),
            ("GROUP CHAT",    "Create rooms, invite users\nand chat as a team",         GLOW,   self._open_group,     1, 0),
            ("CHAT HISTORY",  "Search and browse all\nprevious messages",               PURPLE, self._open_history,   1, 1),
            ("SERVER STATUS", "Live analytics, network\nhealth and message stats",      GLOW,   self._open_status,    2, 0),
            ("DISCONNECT",    "Sign out and close\nSentinelChat securely",             DANGER, self._exit,           2, 1),
        ]

        for title, desc, color, cmd, r, c in CARDS:
            self._make_card(grid, title, desc, color, cmd, r, c)

        # ── Footer ────────────────────────────────────────────
        foot = tk.Frame(self.root, bg=PANEL, height=32)
        foot.pack(side="bottom", fill="x")
        foot.pack_propagate(False)

        tk.Frame(foot, bg=PURPLE, height=1).place(relx=0, rely=0, relwidth=1)

        tk.Label(foot, text=f"  {self.username}",
                 font=("Segoe UI", 9), fg=MUTED, bg=PANEL).pack(side="left", padx=14, pady=7)
        tk.Label(foot, text="● SERVER ONLINE",
                 font=("Segoe UI", 9, "bold"), fg=SUCCESS, bg=PANEL).pack(side="left", expand=True)
        tk.Label(foot, text="ISEA Summer Internship 2026  ",
                 font=("Segoe UI", 9), fg=MUTED, bg=PANEL).pack(side="right")

    # ─────────────────────────────────────────────────────────
    def _make_card(self, parent, title, desc, accent, cmd, row, col):
        outer = tk.Frame(parent, bg=BG)
        outer.grid(row=row, column=col, padx=10, pady=8, sticky="nsew")

        # Dual-color border: thin frame with accent color
        border = tk.Frame(outer, bg=accent, padx=1, pady=1)
        border.pack(fill="both", expand=True)

        card = tk.Frame(border, bg=CARD, cursor="hand2")
        card.pack(fill="both", expand=True)

        # Inner layout: left accent bar + content + arrow
        inner = tk.Frame(card, bg=CARD)
        inner.pack(fill="both", expand=True, padx=0, pady=0)

        # Left color bar (3px)
        bar = tk.Frame(inner, bg=accent, width=3)
        bar.pack(side="left", fill="y")

        # Content
        content = tk.Frame(inner, bg=CARD)
        content.pack(side="left", fill="both", expand=True, padx=18, pady=14)

        # Title row
        title_row = tk.Frame(content, bg=CARD)
        title_row.pack(fill="x", anchor="w")

        # Accent dot
        dot = tk.Label(title_row, text="◆",
                       font=("Segoe UI", 8), fg=accent, bg=CARD)
        dot.pack(side="left", pady=(2, 0))

        ttl = tk.Label(title_row, text=f"  {title}",
                       font=("Segoe UI", 13, "bold"), bg=CARD, fg=TEXT)
        ttl.pack(side="left")

        dsc = tk.Label(content, text=desc,
                       font=("Segoe UI", 9), bg=CARD, fg=MUTED,
                       justify="left", anchor="w")
        dsc.pack(anchor="w", pady=(5, 0))

        # Arrow
        arr = tk.Label(inner, text="→",
                       font=("Segoe UI", 14, "bold"), bg=CARD, fg=MUTED)
        arr.pack(side="right", padx=16)

        all_w = [card, inner, bar, content, title_row, dot, ttl, dsc, arr]

        def on_enter(e=None):
            card.config(bg=CARD_H)
            inner.config(bg=CARD_H)
            content.config(bg=CARD_H)
            title_row.config(bg=CARD_H)
            for w in [dot, ttl, dsc, arr]: w.config(bg=CARD_H)
            arr.config(fg=accent)
            border.config(bg=accent)

        def on_leave(e=None):
            card.config(bg=CARD)
            inner.config(bg=CARD)
            content.config(bg=CARD)
            title_row.config(bg=CARD)
            for w in [dot, ttl, dsc, arr]: w.config(bg=CARD)
            arr.config(fg=MUTED)
            border.config(bg=accent)

        def on_click(e=None):
            # Flash white then accent — gives tactile click feel
            border.config(bg="#FFFFFF")
            self.root.after(80,  lambda: border.config(bg=GLOW))
            self.root.after(160, lambda: border.config(bg=accent))
            self.root.after(220, cmd)

        for w in all_w + [border]:
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)
            w.bind("<Button-1>", on_click)

    # ─────────────────────────────────────────────────────────
    def _clock_tick(self):
        self.clock.config(text=time.strftime("%H:%M:%S"))
        aid = self.root.after(1000, self._clock_tick)
        self._after_ids.append(aid)

    def _heartbeat(self):
        self.hb_dot.config(fg=SUCCESS if self._tick_on else PANEL)
        self._tick_on = not self._tick_on
        aid = self.root.after(700, self._heartbeat)
        self._after_ids.append(aid)

    # ─────────────────────────────────────────────────────────
    def _open_broadcast(self):
        try:
            from broadcast import Broadcast
            Broadcast(self.username, self.client)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _open_private(self):
        try:
            from private_chat import PrivateChat
            PrivateChat(self.username, self.client)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _open_group(self):
        try:
            from group_chat import GroupChat
            GroupChat(self.username, self.client)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _open_history(self):
        try:
            from history import History
            History(self.username, self.client)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _open_status(self):
        try:
            from status import Status
            Status(self.username, self.client)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _exit(self):
        if messagebox.askyesno("Disconnect", "Sign out and close SentinelChat?"):
            try:
                if self.client: self.client.close()
            except: pass
            self.root.destroy()


if __name__ == "__main__":
    Dashboard("MUSKAN")
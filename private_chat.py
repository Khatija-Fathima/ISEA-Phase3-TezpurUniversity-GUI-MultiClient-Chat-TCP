import tkinter as tk
from tkinter import messagebox
import threading
import time

from ui_fx import GlowPulse, add_bubble_tags, add_bubble, add_system

BG        = "#07111F"
PANEL     = "#0F1A30"
CARD      = "#16233A"
CARD2     = "#1A2940"
TITLE     = "#00D4FF"
GLOW      = "#00D4FF"
TEXT      = "#F8FAFC"
SECONDARY = "#94A3B8"
MUTED     = "#4A5580"
SUCCESS   = "#22C55E"
INPUT_BG  = "#0D1B2E"
BUBBLE_ME   = "#0E3A56"
BUBBLE_THEM = CARD2

PALETTE = dict(TEXT=TEXT, MUTED=SECONDARY, SUCCESS=SUCCESS,
               BUBBLE_ME=BUBBLE_ME, BUBBLE_THEM=BUBBLE_THEM)


class PrivateChat:

    def __init__(self, username, client=None):
        self.username = username
        self.client   = client
        self.selected_user = tk.StringVar(value="")
        self._running  = True
        self._pulses   = []

        self.root = tk.Toplevel()
        self.root.title("SentinelChat — Private Chat")
        self.root.geometry("900x660")
        self.root.minsize(700, 500)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build()
        self._welcome_state()

        if self.client:
            threading.Thread(
                target=self._receive_loop,
                daemon=True
            ).start()

        self.root.after(400, self._refresh_users)

    # ──────────────────────────────────────────────────────────
    def _build(self):

        # ── TOP BAR ──────────────────────────────────────────
        top = tk.Frame(self.root, bg=PANEL, height=54)
        top.pack(side="top", fill="x")
        top.pack_propagate(False)

        title_frame = tk.Frame(top, bg=PANEL)
        title_frame.pack(side="left", padx=20)

        tk.Label(
            title_frame,
            text="◈ PRIVATE CHANNEL",
            font=("Segoe UI",16,"bold"),
            fg=TITLE,
            bg=PANEL
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="End-to-End Secure Communication",
            font=("Segoe UI",9),
            fg=SECONDARY,
            bg=PANEL
        ).pack(anchor="w")

        user_box = tk.Frame(top, bg=CARD2, padx=10, pady=4)
        user_box.pack(side="right", padx=18)

        tk.Label(
            user_box,
            text=f"● {self.username.upper()}",
            font=("Segoe UI",10,"bold"),
            fg=SUCCESS,
            bg=CARD2
        ).pack()

        self.chat_header = tk.Label(
            top, text="← Select a user to start the chat",
            font=("Segoe UI", 10), fg=SECONDARY, bg=PANEL
        )
        self.chat_header.pack(side="left", padx=10)
        self.status_lbl = tk.Label(
            top,
            text="Waiting for secure channel...",
            font=("Segoe UI", 8),
            fg=MUTED,
            bg=PANEL
        )
        self.status_lbl.pack(side="left", padx=8)

        # ── FOOTER (packed early so it anchors to bottom) ────
        footer = tk.Frame(self.root, bg=PANEL, height=28)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)
        tk.Label(footer, text="ISEA Summer Internship 2026",
                 font=("Segoe UI", 8), fg=SECONDARY, bg=PANEL).pack(expand=True)

        # ── INPUT BAR (packed before body so it stays above footer) ──
        input_bar = tk.Frame(self.root, bg=PANEL)
        input_bar.pack(side="bottom", fill="x", padx=0, pady=0)

        inner = tk.Frame(input_bar, bg=PANEL, pady=10)
        inner.pack(fill="x", padx=14)

        # Glowing border around input — breathes gently while idle
        entry_border = tk.Frame(inner, bg=MUTED, padx=1, pady=1)
        entry_border.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.msg_entry = tk.Entry(
            entry_border, font=("Segoe UI", 12),
            bg="#0A1628", fg=TEXT, insertbackground=GLOW,
            relief="flat"
        )
        self.msg_entry.pack(fill="x", ipady=10, padx=1, pady=1)
        self.msg_entry.bind("<Return>", self.send)

        # Placeholder
        self.msg_entry.insert(0, "Type a message...")
        self.msg_entry.config(fg=MUTED)

        entry_pulse = GlowPulse(entry_border, MUTED, "#1E3A6E", period_ms=2600)
        entry_pulse.start()
        self._pulses.append(entry_pulse)

        def on_focus_in(e):
            if self.msg_entry.get() == "Type a message...":
                self.msg_entry.delete(0, "end")
                self.msg_entry.config(fg=TEXT)
            entry_pulse.stop(hold=GLOW)

        def on_focus_out(e):
            if not self.msg_entry.get():
                self.msg_entry.insert(0, "Type a message...")
                self.msg_entry.config(fg=MUTED)
            entry_pulse.start()

        self.msg_entry.bind("<FocusIn>",  on_focus_in)
        self.msg_entry.bind("<FocusOut>", on_focus_out)

        send_btn = tk.Button(
            inner, text="SEND  ▶",
            bg=TITLE, fg="#000000",
            activebackground="#42E5FF", activeforeground="#000000",
            relief="flat", cursor="hand2",
            font=("Segoe UI", 11, "bold"), padx=18, pady=6,
            command=self.send
        )
        send_btn.pack(side="right")
        send_btn.bind("<Enter>", lambda e: send_btn.config(bg="#42E5FF"))
        send_btn.bind("<Leave>", lambda e: send_btn.config(bg=TITLE))

        # ── BODY (fills remaining space) ─────────────────────
        body = tk.Frame(self.root, bg=BG)
        body.pack(side="top", fill="both", expand=True)

        # Left — user list
        left = tk.Frame(body, bg=PANEL, width=190)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        head_row = tk.Frame(left, bg=PANEL)
        head_row.pack(fill="x", pady=(14, 4), padx=14)
        tk.Label(head_row, text="ONLINE USERS",
                 font=("Segoe UI", 9, "bold"), fg=SECONDARY, bg=PANEL).pack(side="left")
        self.online_count = tk.Label(head_row, text="0",
                                      font=("Segoe UI", 9, "bold"), fg=TITLE, bg=PANEL)
        self.online_count.pack(side="right")

        self.user_list = tk.Listbox(
            left, bg=PANEL, fg=TEXT,
            font=("Segoe UI", 11),
            relief="flat",
            selectbackground=CARD2, selectforeground=TITLE,
            activestyle="none", highlightthickness=0, borderwidth=0
        )
        self.user_list.pack(fill="both", expand=True, padx=6, pady=(0, 4))
        self.user_list.bind("<<ListboxSelect>>", self._select_user)

        refresh_btn = tk.Button(
            left, text="⟳  Refresh",
            bg=CARD, fg=SECONDARY,
            relief="flat", cursor="hand2",
            font=("Segoe UI", 9),
            command=self._refresh_users
        )
        refresh_btn.pack(fill="x", padx=8, pady=(0, 10))
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(fg=TITLE))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(fg=SECONDARY))

        # Right — chat display
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self.chat_display = tk.Text(
            right,
            font=("Segoe UI", 10),
            bg=INPUT_BG, fg=TEXT,
            relief="flat", state="disabled",
            wrap="word", padx=12, pady=12,
            spacing1=4, spacing3=4, cursor="arrow"
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=8)
        add_bubble_tags(self.chat_display, PALETTE)

    # ──────────────────────────────────────────────────────────
    def _welcome_state(self):
        add_system(self.chat_display,
                    "🔐 Messages are routed securely through the server.\n"
                    "Select a user on the left to start a conversation.")

    # ──────────────────────────────────────────────────────────
    def _receive_loop(self):
        while self._running:
            try:
                msg = self.client.recv(4096).decode()
                if not msg:
                    break
                self.root.after(0, self._handle_incoming, msg)
            except Exception:
                break

    def _handle_incoming(self, msg):
        ts = time.strftime("%H:%M")
        if msg.startswith("[PRIVATE]"):
            body = msg[len("[PRIVATE] "):]
            sender, _, text = body.partition(":")
            add_bubble(self.chat_display, "them", sender.strip(), text.strip(), ts)
        elif msg.startswith("[BROADCAST]"):
            body = msg[len("[BROADCAST] "):]
            add_system(self.chat_display, f"📡 Broadcast — {body}")
        elif msg.startswith("[GROUP"):
            add_system(self.chat_display, f"👥 {msg}")
        elif msg.startswith("Online Users:"):
            lines = msg.split("\n")[1:]
            self.user_list.delete(0, "end")
            count = 0
            for name in lines:
                name = name.strip()
                if name and name.upper() != self.username.upper():
                    self.user_list.insert("end", f"  🟢 {name}")
                    count += 1
            self.online_count.config(text=str(count))
        else:
            add_system(self.chat_display, msg)

    # ──────────────────────────────────────────────────────────
    def _select_user(self, event=None):
        sel = self.user_list.curselection()
        if sel:
            raw = self.user_list.get(sel[0]).strip().replace("🟢", "").strip()
            self.selected_user.set(raw)
            self.chat_header.config(
                text=f"🟢 {raw.upper()}",
                fg=SUCCESS
            )
            self.status_lbl.config(
                text="Encrypted Channel Established",
                fg=TITLE
            )
            add_system(self.chat_display, f"Conversation with {raw} opened.")
            self.msg_entry.focus()

    def _refresh_users(self):
        try:
            if self.client:
                self.client.send("/list".encode())
        except Exception:
            pass

    def send(self, event=None):
        target = self.selected_user.get()
        msg    = self.msg_entry.get().strip()
        if msg == "Type a message...":
            return

        if not target:
            messagebox.showwarning("No User Selected",
                                   "Click a name in the ONLINE USERS list first.")
            return
        if not msg:
            return

        try:
            if self.client:
                self.client.send(f"/msg {target} {msg}".encode())
            ts = time.strftime("%H:%M")
            add_bubble(self.chat_display, "me", "You", msg, ts)
            self.msg_entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Send Error", str(e))

    def _on_close(self):
        self._running = False
        for p in self._pulses:
            p.stop()
        self.root.destroy()


if __name__ == "__main__":
    PrivateChat("MUSKAN")
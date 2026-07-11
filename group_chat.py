import tkinter as tk
from tkinter import messagebox, simpledialog
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


class GroupChat:

    def __init__(self, username, client=None):
        self.username      = username
        self.client        = client
        self.current_group = tk.StringVar(value="")
        self._running      = True
        self._pulses       = []

        self.root = tk.Toplevel()
        self.root.title("SentinelChat — Group Chat")
        self.root.geometry("940x680")
        self.root.minsize(700, 500)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build()
        self._welcome_state()

        if self.client:
            threading.Thread(target=self._receive_loop, daemon=True).start()

    # ──────────────────────────────────────────────────────────
    def _build(self):

        # ── TOP BAR ──────────────────────────────────────────
        top = tk.Frame(self.root, bg=PANEL, height=54)
        top.pack(side="top", fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="👥  GROUP CHAT",
                 font=("Segoe UI", 15, "bold"), fg=TITLE, bg=PANEL
                 ).pack(side="left", padx=20, pady=10)

        tk.Label(top, text=f"👤 {self.username}",
                 font=("Segoe UI", 10), fg=SECONDARY, bg=PANEL
                 ).pack(side="right", padx=20)

        self.group_header = tk.Label(
            top, text="← Select or create a group",
            font=("Segoe UI", 10), fg=SECONDARY, bg=PANEL
        )
        self.group_header.pack(side="left", padx=10)

        # ── FOOTER ───────────────────────────────────────────
        footer = tk.Frame(self.root, bg=PANEL, height=28)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)
        tk.Label(footer, text="ISEA Summer Internship 2026",
                 font=("Segoe UI", 8), fg=SECONDARY, bg=PANEL).pack(expand=True)

        # ── INPUT BAR ────────────────────────────────────────
        input_bar = tk.Frame(self.root, bg=PANEL)
        input_bar.pack(side="bottom", fill="x")

        inner = tk.Frame(input_bar, bg=PANEL, pady=10)
        inner.pack(fill="x", padx=14)

        # Glowing border around input — breathes gently while idle
        entry_border = tk.Frame(inner, bg=MUTED, padx=1, pady=1)
        entry_border.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.msg_entry = tk.Entry(
            entry_border, font=("Segoe UI", 12),
            bg="#0A1628", fg=TEXT, insertbackground=TITLE,
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
            entry_pulse.stop(hold=TITLE)

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

        # ── BODY ─────────────────────────────────────────────
        body = tk.Frame(self.root, bg=BG)
        body.pack(side="top", fill="both", expand=True)

        # Left — group list
        left = tk.Frame(body, bg=PANEL, width=210)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="GROUPS",
                 font=("Segoe UI", 9, "bold"), fg=SECONDARY, bg=PANEL
                 ).pack(pady=(14, 6), padx=14, anchor="w")

        self.group_list = tk.Listbox(
            left, bg=PANEL, fg=TEXT, font=("Segoe UI", 11),
            relief="flat", selectbackground=CARD2,
            selectforeground=TITLE, activestyle="none",
            highlightthickness=0, borderwidth=0
        )
        self.group_list.pack(fill="both", expand=True, padx=6, pady=(0, 4))
        self.group_list.bind("<<ListboxSelect>>", self._select_group)

        btn_frame = tk.Frame(left, bg=PANEL)
        btn_frame.pack(fill="x", padx=8, pady=(0, 10))

        create_btn = tk.Button(btn_frame, text="＋  Create Group",
                  bg=TITLE, fg="black", relief="flat", cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  command=self._create_group)
        create_btn.pack(fill="x", pady=(0, 4))
        create_btn.bind("<Enter>", lambda e: create_btn.config(bg="#42E5FF"))
        create_btn.bind("<Leave>", lambda e: create_btn.config(bg=TITLE))

        join_btn = tk.Button(btn_frame, text="→  Join Group",
                  bg=CARD, fg=SECONDARY, relief="flat", cursor="hand2",
                  font=("Segoe UI", 9),
                  command=self._join_group)
        join_btn.pack(fill="x")
        join_btn.bind("<Enter>", lambda e: join_btn.config(fg=TITLE))
        join_btn.bind("<Leave>", lambda e: join_btn.config(fg=SECONDARY))

        # Right — chat
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self.chat_display = tk.Text(
            right, font=("Segoe UI", 10),
            bg=INPUT_BG, fg=TEXT, relief="flat",
            state="disabled", wrap="word",
            padx=12, pady=12, spacing1=4, spacing3=4, cursor="arrow"
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=8)
        add_bubble_tags(self.chat_display, PALETTE)

    # ──────────────────────────────────────────────────────────
    def _welcome_state(self):
        add_system(self.chat_display,
                    "👥 Create or join a group to start chatting.\n"
                    "Everyone in the group sees every message.")

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
        if msg.startswith("[GROUP"):
            # Format from server: "[GROUP <name>] <sender>: <text>"
            try:
                header, rest = msg.split("]", 1)
                sender, _, text = rest.strip().partition(":")
                sender = sender.strip()
                text = text.strip()
            except Exception:
                sender, text = "GROUP", msg

            if sender.upper() == self.username.upper():
                return  # avoid double-showing our own echoed message

            add_bubble(self.chat_display, "them", sender, text, ts)
        elif msg.startswith("[PRIVATE]"):
            body = msg[len("[PRIVATE] "):]
            add_system(self.chat_display, f"🔐 Private — {body}")
        elif msg.startswith("[BROADCAST]"):
            body = msg[len("[BROADCAST] "):]
            add_system(self.chat_display, f"📡 Broadcast — {body}")
        elif "created" in msg.lower() or "joined" in msg.lower():
            add_system(self.chat_display, msg)
        else:
            add_system(self.chat_display, msg)

    # ──────────────────────────────────────────────────────────
    def _select_group(self, event=None):
        sel = self.group_list.curselection()
        if sel:
            raw = self.group_list.get(sel[0]).strip().lstrip("#").strip()
            self.current_group.set(raw)
            self.group_header.config(text=f"👥  #{raw}", fg=TITLE)
            add_system(self.chat_display, f"Active group: #{raw}")
            self.msg_entry.focus()

    def _create_group(self):
        name = simpledialog.askstring("Create Group", "Group name:", parent=self.root)
        if name:
            name = name.strip()
            if name:
                try:
                    if self.client:
                        self.client.send(f"/group create {name}".encode())
                    self.group_list.insert("end", f"  # {name}")
                    add_system(self.chat_display, f"Group #{name} created.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def _join_group(self):
        name = simpledialog.askstring("Join Group", "Group name to join:", parent=self.root)
        if name:
            name = name.strip()
            if name:
                try:
                    if self.client:
                        self.client.send(f"/group join {name}".encode())
                    if f"  # {name}" not in [self.group_list.get(i) for i in range(self.group_list.size())]:
                        self.group_list.insert("end", f"  # {name}")
                    self.current_group.set(name)
                    self.group_header.config(text=f"👥  #{name}", fg=TITLE)
                    add_system(self.chat_display, f"Joined #{name}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def send(self, event=None):
        group = self.current_group.get()
        msg   = self.msg_entry.get().strip()
        if msg == "Type a message...":
            return

        if not group:
            messagebox.showwarning("No Group", "Select or join a group first.")
            return
        if not msg:
            return

        try:
            if self.client:
                self.client.send(f"/group {group} {msg}".encode())
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
    GroupChat("MUSKAN")
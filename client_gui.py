import tkinter as tk
from tkinter import messagebox
import socket
import math

PORT = 5000

BG       = "#050510"
PANEL    = "#0A0A1F"
CARD     = "#0D0D24"
GLOW     = "#00D4FF"
PURPLE   = "#8B5CF6"
TEXT     = "#E8F0FF"
MUTED    = "#3A4060"
SUCCESS  = "#22C55E"
DANGER   = "#EF4444"
INPUT_BG = "#07071A"


class LoginWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("SentinelChat")
        self.root.geometry("520x640")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._phase = 0.0
        self.lock_time = 30

        self._build()
        self._animate()

        self.root.mainloop()

    def _build(self):

        # Top animated bar
        bar_frame = tk.Frame(self.root, height=3, bg=BG)
        bar_frame.pack(fill="x")

        self._top_canvas = tk.Canvas(
            bar_frame,
            height=3,
            bg=BG,
            highlightthickness=0
        )
        self._top_canvas.pack(fill="x")

        # Logo
        logo = tk.Frame(self.root, bg=BG)
        logo.pack(pady=(36, 0))

        self._logo_canvas = tk.Canvas(
            logo,
            width=60,
            height=60,
            bg=BG,
            highlightthickness=0
        )

        self._logo_canvas.pack()

        pts = [30,4,56,30,30,56,4,30]

        self._logo_canvas.create_polygon(
            pts,
            outline=GLOW,
            fill="",
            width=2
        )

        self._logo_canvas.create_polygon(
            pts,
            outline=PURPLE,
            fill="",
            width=1,
            dash=(4,4)
        )

        self._logo_canvas.create_oval(
            22,22,38,38,
            outline=GLOW,
            fill=BG,
            width=1
        )

        tk.Label(
            logo,
            text="SENTINEL CHAT",
            font=("Segoe UI",22,"bold"),
            fg=TEXT,
            bg=BG
        ).pack(pady=(10,0))

        tk.Label(
            logo,
            text="SECURE  ·  ENCRYPTED  ·  REAL-TIME",
            font=("Segoe UI",8),
            fg=MUTED,
            bg=BG
        ).pack(pady=(4,0))

        # Card
        outer = tk.Frame(
            self.root,
            bg=PURPLE,
            padx=1,
            pady=1
        )

        outer.pack(
            padx=40,
            pady=24,
            fill="x"
        )

        inner = tk.Frame(
            outer,
            bg=GLOW,
            padx=1,
            pady=1
        )

        inner.pack(fill="x")

        card = tk.Frame(
            inner,
            bg=CARD
        )

        card.pack(fill="x")

        form = tk.Frame(
            card,
            bg=CARD
        )

        form.pack(
            padx=28,
            pady=28,
            fill="x"
        )

                # ===========================
        # SERVER IP
        # ===========================

        tk.Label(
            form,
            text="SERVER IP",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w")

        self._ip_border = tk.Frame(
            form,
            bg=MUTED,
            padx=1,
            pady=1
        )

        self._ip_border.pack(fill="x", pady=(4,16))

        self.server_ip = tk.Entry(
            self._ip_border,
            font=("Segoe UI Mono",11),
            bg=INPUT_BG,
            fg=GLOW,
            insertbackground=GLOW,
            relief="flat",
            bd=0
        )

        self.server_ip.pack(fill="x", ipady=9, padx=2, pady=1)

        self.server_ip.insert(0,"127.0.0.1")

        self.server_ip.bind(
            "<FocusIn>",
            lambda e:self._ip_border.config(bg=GLOW)
        )

        self.server_ip.bind(
            "<FocusOut>",
            lambda e:self._ip_border.config(bg=MUTED)
        )

        # ===========================
        # USERNAME
        # ===========================

        tk.Label(
            form,
            text="USERNAME",
            font=("Segoe UI",8,"bold"),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w")

        self._user_border = tk.Frame(
            form,
            bg=MUTED,
            padx=1,
            pady=1
        )

        self._user_border.pack(fill="x", pady=(4,0))

        self.username = tk.Entry(
            self._user_border,
            font=("Segoe UI",11),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=GLOW,
            relief="flat",
            bd=0
        )

        self.username.pack(fill="x", ipady=9, padx=2, pady=1)

        self.username.bind(
            "<FocusIn>",
            lambda e:self._user_border.config(bg=PURPLE)
        )

        self.username.bind(
            "<FocusOut>",
            lambda e:self._user_border.config(bg=MUTED)
        )

        self.username.bind(
            "<Return>",
            lambda e:self._connect()
        )

        # ===========================
        # PASSWORD
        # ===========================

        tk.Label(
            form,
            text="PASSWORD",
            font=("Segoe UI",8,"bold"),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w", pady=(16,0))

        self._pass_border = tk.Frame(
            form,
            bg=MUTED,
            padx=1,
            pady=1
        )

        self._pass_border.pack(fill="x", pady=(4,0))

        self.password = tk.Entry(
            self._pass_border,
            font=("Segoe UI",11),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=GLOW,
            relief="flat",
            bd=0,
            show="*"
        )

        self.password.pack(fill="x", ipady=9, padx=2, pady=1)

        self.show_password = False

        self.show_btn = tk.Button(
            self._pass_border,
            text="👁",
            font=("Segoe UI Emoji", 10),
            bg=INPUT_BG,
            fg=GLOW,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.toggle_password
        )

        self.show_btn.place(relx=0.97, rely=0.5, anchor="e")

        self.password.bind(
            "<FocusIn>",
            lambda e:self._pass_border.config(bg=PURPLE)
        )

        self.password.bind(
            "<FocusOut>",
            lambda e:self._pass_border.config(bg=MUTED)
        )

        self.password.bind(
            "<Return>",
            lambda e:self._connect()
        )

        # ===========================
        # STATUS
        # ===========================

        status_row = tk.Frame(
            form,
            bg=CARD
        )

        status_row.pack(fill="x", pady=(18,0))

        self.status_dot = tk.Label(
            status_row,
            text="●",
            font=("Segoe UI",10),
            fg=DANGER,
            bg=CARD
        )

        self.status_dot.pack(side="left")

        self.status_lbl = tk.Label(
            status_row,
            text="  Not Connected",
            font=("Segoe UI",9),
            fg=MUTED,
            bg=CARD
        )

        self.status_lbl.pack(side="left")

        # ===========================
        # CONNECT BUTTON
        # ===========================

        self.btn = tk.Button(
            self.root,
            text="CONNECT ▶",
            font=("Segoe UI",12,"bold"),
            bg=GLOW,
            fg="#000000",
            activebackground=PURPLE,
            activeforeground=TEXT,
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=13,
            command=self._connect
        )

        self.btn.pack(
            padx=40,
            fill="x"
        )

        self.btn.bind(
            "<Enter>",
            lambda e:self.btn.config(bg=PURPLE,fg=TEXT)
        )

        self.btn.bind(
            "<Leave>",
            lambda e:self.btn.config(bg=GLOW,fg="#000000")
        )

        # ===========================
        # FOOTER
        # ===========================

        tk.Label(
            self.root,
            text="ISEA Summer Internship 2026  ·  SentinelChat v2.0",
            font=("Segoe UI",8),
            fg=MUTED,
            bg=BG
        ).pack(
            side="bottom",
            pady=12
        )

    def _animate(self):
        """Animate top glow bar and logo."""

        self._phase = (self._phase + 0.04) % (2 * math.pi)
        t = (math.sin(self._phase) + 1) / 2

        def lerp(a, b, t):
            return int(a + (b - a) * t)

        cyan = (0x00, 0xD4, 0xFF)
        purple = (0x8B, 0x5C, 0xF6)

        r = lerp(cyan[0], purple[0], t)
        g = lerp(cyan[1], purple[1], t)
        b = lerp(cyan[2], purple[2], t)

        color = f"#{r:02x}{g:02x}{b:02x}"

        width = self.root.winfo_width()

        self._top_canvas.config(
            bg=color,
            width=width
        )

        try:
            self._logo_canvas.itemconfig(1, outline=color)
        except Exception:
            pass

        self.root.after(40, self._animate)
   
    def _start_lock_timer(self):

        if self.lock_time > 0:

            self.btn.config(
                text=f"WAIT {self.lock_time}s",
                state="disabled",
                bg=MUTED,
                fg=TEXT
            )

            self.status_lbl.config(
                text=f"  Account Locked ({self.lock_time}s)",
                fg=DANGER
            )

            self.lock_time -= 1

            self.root.after(
                1000,
                self._start_lock_timer
            )

        else:

            self.lock_time = 30

            self.btn.config(
                text="CONNECT ▶",
                state="normal",
                bg=GLOW,
                fg="#000000"
            )

            self.status_dot.config(
                fg=DANGER
            )

            self.status_lbl.config(
                text="  Not Connected",
                fg=MUTED
            )

    def toggle_password(self):

        self.show_password = not self.show_password

        if self.show_password:
            self.password.config(show="")
            self.show_btn.config(text="Hide")
        else:
            self.password.config(show="*")
            self.show_btn.config(text="Show")


    def _connect(self):

        ip = self.server_ip.get().strip()
        user = self.username.get().strip()
        password = self.password.get().strip()

        if not ip:
            messagebox.showerror(
                "Error",
                "Enter server IP."
            )
            return

        if not user:
            messagebox.showerror(
                "Error",
                "Enter username."
            )
            return

        if not password:
            messagebox.showerror(
                "Error",
                "Enter password."
            )
            return

        self.btn.config(
            text="CONNECTING...",
            state="disabled",
            bg=MUTED,
            fg=TEXT
        )

        self.status_dot.config(
            fg=MUTED
        )

        self.status_lbl.config(
            text="  Connecting...",
            fg=MUTED
        )

        self.root.update()

        try:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(5)

            sock.connect((ip, PORT))

            login_packet = f"LOGIN|{user}|{password}"

            sock.send(login_packet.encode())

            response = sock.recv(1024).decode()

            sock.settimeout(None)

            if response == "LOGIN_SUCCESS":

                self.status_dot.config(
                    fg=SUCCESS
                )

                self.status_lbl.config(
                    text="  Authentication Successful",
                    fg=SUCCESS
                )

                self.root.update()

                self.root.after(
                    500,
                    lambda: self._open_dashboard(
                        user,
                        sock
                    )
                )

            elif response == "DUPLICATE_LOGIN":

                sock.close()

                self.btn.config(
                    text="CONNECT ▶",
                    state="normal",
                    bg=GLOW,
                    fg="#000000"
                )

                self.status_dot.config(fg=DANGER)
                self.status_lbl.config(
                    text="  User Already Logged In",
                    fg=DANGER
                )

                messagebox.showerror(
                    "Duplicate Login",
                    "This user is already logged in."
                )

                return

            elif response == "ACCOUNT_LOCKED":

                sock.close()

                self.btn.config(
                    text="CONNECT ▶",
                    state="normal",
                    bg=GLOW,
                    fg="#000000"
                )

                self.status_dot.config(fg=DANGER)

                self.status_lbl.config(
                    text="  Account Locked",
                    fg=DANGER
                )

                messagebox.showerror(
                    "Account Locked",
                    "Too many failed login attempts.\nTry again after 30 seconds."
                )
                self.lock_time = 30
                self._start_lock_timer()
                return

            else:

                sock.close()

                self.btn.config(
                    text="CONNECT ▶",
                    state="normal",
                    bg=GLOW,
                    fg="#000000"
                )

                self.status_dot.config(fg=DANGER)
                self.status_lbl.config(
                    text="  Login Failed",
                    fg=DANGER
                )

                messagebox.showerror(
                    "Authentication Failed",
                    "Invalid username or password."
                )

                return

        except Exception as e:

            self.btn.config(
                text="CONNECT ▶",
                state="normal",
                bg=GLOW,
                fg="#000000"
            )

            self.status_dot.config(
                fg=DANGER
            )

            self.status_lbl.config(
                text="  Connection Failed",
                fg=DANGER
            )

            messagebox.showerror(
                "Connection Error",
                str(e)
            )

    def _open_dashboard(self, user, sock):
        """
        Close the login window and open the main dashboard.
        """

        self.root.destroy()

        from dashboard import Dashboard

        Dashboard(user, sock)


if __name__ == "__main__":
    LoginWindow()        
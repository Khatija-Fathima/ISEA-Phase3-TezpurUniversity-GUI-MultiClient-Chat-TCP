"""
ui_fx.py — shared visual-effects helpers for SentinelChat.
Pure Tkinter, no external deps. Import and use; never changes networking code.
"""

import math
import time


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)


def lerp_color(c1, c2, t):
    """t in [0,1] -> hex color interpolated between c1 and c2."""
    a = _hex_to_rgb(c1)
    b = _hex_to_rgb(c2)
    return _rgb_to_hex(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))


class GlowPulse:
    """
    Smoothly oscillates a widget's color between two hex colors, forever,
    using a sine wave so it feels like breathing rather than blinking.

    Usage:
        pulse = GlowPulse(border_frame, "#0D1333", "#00D4FF", period_ms=2200)
        pulse.start()
        ...
        pulse.stop()              # freeze wherever it is
        pulse.stop(hold="#00D4FF") # freeze at a specific color (e.g. on hover)
    """

    def __init__(self, widget, color_a, color_b, period_ms=2000, attr="bg", delay_ms=0):
        self.widget = widget
        self.a = color_a
        self.b = color_b
        self.period = max(200, period_ms)
        self.attr = attr
        self.delay = delay_ms
        self._running = False
        self._t0 = None
        self._job = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._t0 = time.time() - (self.delay / 1000.0)
        self._tick()

    def stop(self, hold=None):
        self._running = False
        if self._job:
            try:
                self.widget.after_cancel(self._job)
            except Exception:
                pass
            self._job = None
        if hold:
            try:
                self.widget.configure(**{self.attr: hold})
            except Exception:
                pass

    def set_colors(self, color_a, color_b):
        self.a, self.b = color_a, color_b

    def _tick(self):
        if not self._running:
            return
        elapsed = time.time() - self._t0
        phase = (math.sin(elapsed * 2 * math.pi / (self.period / 1000.0)) + 1) / 2
        try:
            self.widget.configure(**{self.attr: lerp_color(self.a, self.b, phase)})
        except Exception:
            self._running = False
            return
        self._job = self.widget.after(45, self._tick)


def add_bubble_tags(text_widget, palette):
    """
    Configure a tk.Text widget with WhatsApp-style bubble paragraph tags,
    using Text's per-run background + justify + margins (no canvas needed,
    so scrolling/threading/append all keep working exactly as before).

    palette: dict with keys TEXT, MUTED, SUCCESS, BUBBLE_ME, BUBBLE_THEM
    """
    text_widget.tag_config("meta_me", foreground=palette["MUTED"],
                            justify="right", font=("Segoe UI", 8))
    text_widget.tag_config("meta_them", foreground=palette["MUTED"],
                            justify="left", font=("Segoe UI", 8))
    text_widget.tag_config("bubble_me", background=palette["BUBBLE_ME"],
                            foreground=palette["TEXT"], justify="right",
                            lmargin1=110, lmargin2=110, rmargin=14,
                            spacing1=1, spacing3=12, wrap="word",
                            font=("Segoe UI", 10))
    text_widget.tag_config("bubble_them", background=palette["BUBBLE_THEM"],
                            foreground=palette["TEXT"], justify="left",
                            lmargin1=14, lmargin2=14, rmargin=110,
                            spacing1=1, spacing3=12, wrap="word",
                            font=("Segoe UI", 10))
    text_widget.tag_config("system", foreground=palette["SUCCESS"],
                            justify="center", spacing1=4, spacing3=10,
                            font=("Segoe UI", 9, "italic"))


def add_bubble(text_widget, side, label, msg, ts):
    """Insert one meta line + one bubble line. side is 'me' or 'them'."""
    meta_tag = "meta_me" if side == "me" else "meta_them"
    bubble_tag = "bubble_me" if side == "me" else "bubble_them"
    text_widget.config(state="normal")
    text_widget.insert("end", f"{label}  ·  {ts}\n", meta_tag)
    text_widget.insert("end", f"  {msg}  \n", bubble_tag)
    text_widget.config(state="disabled")
    text_widget.see("end")


def add_system(text_widget, msg):
    text_widget.config(state="normal")
    text_widget.insert("end", f"{msg}\n", "system")
    text_widget.config(state="disabled")
    text_widget.see("end")
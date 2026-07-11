import tkinter as tk
import random
import math


class CyberBackground:

    def __init__(self, parent,
                 bg="#07111F",
                 cyan="#00D4FF",
                 purple="#8B5CF6"):

        self.canvas = tk.Canvas(
            parent,
            bg=bg,
            highlightthickness=0,
            bd=0
        )

        self.canvas.place(relx=0, rely=0,
                          relwidth=1,
                          relheight=1)

        self.bg = bg
        self.cyan = cyan
        self.purple = purple

        self.particles = []

        parent.after(200, self._create) 
        
    def _create(self):

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 10:
            self.canvas.after(100, self._create)
            return

        # Grid

        for x in range(0, w, 50):

            self.canvas.create_line(
                x,0,x,h,
                fill="#0B1930"
            )

        for y in range(0,h,50):

            self.canvas.create_line(
                0,y,w,y,
                fill="#0B1930"
            )

        # Particles

        for _ in range(40):

            x=random.randint(0,w)
            y=random.randint(0,h)

            r=random.randint(1,3)

            color=random.choice([
                self.cyan,
                self.purple,
                "#3B82F6"
            ])

            dot=self.canvas.create_oval(
                x-r,y-r,
                x+r,y+r,
                fill=color,
                outline=""
            )

            self.particles.append([
                dot,
                x,
                y,
                random.uniform(-0.4,0.4),
                random.uniform(-0.4,0.4)
            ])

        self.animate()

    def animate(self):

        w=self.canvas.winfo_width()
        h=self.canvas.winfo_height()

        for p in self.particles:

            item,x,y,dx,dy=p

            x+=dx
            y+=dy

            if x<0: x=w
            if x>w: x=0

            if y<0: y=h
            if y>h: y=0

            self.canvas.coords(
                item,
                x-2,y-2,
                x+2,y+2
            )

            p[1]=x
            p[2]=y

        self.canvas.after(
            30,
            self.animate
        )
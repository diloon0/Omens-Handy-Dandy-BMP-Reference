"""
HOME SCREEN
-------------
The very first thing you see when the app opens: a title and a button for
every reference sheet tab. This file builds itself automatically from the
ALL_TABS list in tabs/__init__.py, so you never need to edit this file when
adding a new tab.
"""

import tkinter as tk

from tabs import ALL_TABS

BG_COLOR = "#1f1f2e"


class HomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app

        title = tk.Label(
            self,
            text="Balatro Multiplayer Reference Sheets",
            font=("Segoe UI", 24, "bold"),
            bg=BG_COLOR,
            fg="white",
        )
        title.pack(pady=(50, 10))

        subtitle = tk.Label(
            self,
            text="Choose a reference sheet below",
            font=("Segoe UI", 12),
            bg=BG_COLOR,
            fg="#cccccc",
        )
        subtitle.pack(pady=(0, 30))

        button_area = tk.Frame(self, bg=BG_COLOR)
        button_area.pack()

        # One button per tab, automatically generated from ALL_TABS.
        for tab_class in ALL_TABS:
            btn = tk.Button(
                button_area,
                text=tab_class.TAB_NAME,
                font=("Segoe UI", 14),
                width=28,
                height=2,
                bg="#3a3a55",
                fg="white",
                activebackground="#50507a",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=lambda tid=tab_class.TAB_ID: self.app.show_frame(tid),
            )
            btn.pack(pady=8)

        if not ALL_TABS:
            empty_label = tk.Label(
                button_area,
                text="No tabs yet - add one in tabs/__init__.py",
                bg=BG_COLOR, fg="#888899", font=("Segoe UI", 11, "italic"),
            )
            empty_label.pack(pady=20)
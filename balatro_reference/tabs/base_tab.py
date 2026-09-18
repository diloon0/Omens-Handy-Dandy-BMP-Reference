"""
BASE TAB
----------
Every reference-sheet tab should inherit from this class so it automatically
gets a "< Home" button and a title bar for free, and so every tab looks and
behaves consistently.

TO MAKE A NEW TAB:
  1. Set TAB_ID   -> a short, unique, lowercase id, e.g. "tarot_odds"
  2. Set TAB_NAME -> the text shown on the home screen button
  3. Override build_content(self) and add your widgets inside self.content

See tabs/tarot_odds.py for a full working example.
"""

import tkinter as tk

BG_COLOR = "#1f1f2e"
HEADER_COLOR = "#151521"


class BaseTab(tk.Frame):

    TAB_ID = "base_tab"      # override this in your subclass
    TAB_NAME = "Base Tab"    # override this in your subclass

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_COLOR)
        self.app = app

        header = tk.Frame(self, bg=HEADER_COLOR)
        header.pack(fill="x", side="top")

        home_btn = tk.Button(
            header,
            text="< Home",
            font=("Segoe UI", 11),
            bg="#3a3a55",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.app.show_frame("home"),
        )
        home_btn.pack(side="left", padx=10, pady=10)

        title = tk.Label(
            header,
            text=self.TAB_NAME,
            font=("Segoe UI", 16, "bold"),
            bg=HEADER_COLOR,
            fg="white",
        )
        title.pack(side="left", padx=10)

        # Subclasses should put all of their own widgets inside this frame.
        self.content = tk.Frame(self, bg=BG_COLOR)
        self.content.pack(fill="both", expand=True)

        self.build_content()

    def build_content(self):
        """Override this in your subclass to add your tab's widgets."""
        pass
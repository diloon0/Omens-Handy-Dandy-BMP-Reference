"""
Balatro Multiplayer Mod Reference Sheets
==========================================
This is the starting point of the program. Run this file to launch the app:

    python main.py

HOW TO ADD A NEW REFERENCE SHEET TAB:
  1. Create a new file in the `tabs/` folder (copy `tabs/tarot_odds.py` as a
     starting template - it's the simplest full example).
  2. Make your new tab a class that inherits from `BaseTab`
     (see `tabs/base_tab.py` for what you get for free).
  3. Open `tabs/__init__.py` and add your new tab class to the ALL_TABS list.
That's it - it will automatically show up as a button on the home screen.
"""

import tkinter as tk

from home_screen import HomeScreen
from tabs import ALL_TABS


class BalatroReferenceApp(tk.Tk):
    """
    The main application window. It doesn't draw much itself - its job is to
    hold every screen (the home screen + every tab) and show/hide them.
    """

    def __init__(self):
        super().__init__()
        self.title("Balatro Multiplayer Reference Sheets")
        self.geometry("1150x780")
        self.minsize(850, 600)
        self.configure(bg="#1f1f2e")

        # The "container" is where every screen lives, stacked on top of
        # each other. We just raise whichever one we want to see. This is a
        # very common, simple pattern for multi-screen tkinter apps.
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create the home screen.
        home_screen = HomeScreen(parent=container, app=self)
        self.frames["home"] = home_screen
        home_screen.grid(row=0, column=0, sticky="nsew")

        # Create every tab listed in tabs/__init__.py automatically.
        for tab_class in ALL_TABS:
            frame = tab_class(parent=container, app=self)
            self.frames[tab_class.TAB_ID] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("home")

    def show_frame(self, frame_id):
        """Raise the requested screen so the user can see it."""
        frame = self.frames[frame_id]
        frame.tkraise()


if __name__ == "__main__":
    app = BalatroReferenceApp()
    app.mainloop()
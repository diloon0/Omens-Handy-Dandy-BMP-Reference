"""
TAROT ODDS TAB
----------------
Shows every tarot card in the game, grouped by type, so you can quickly mark
which ones are useful right now and see the expected value of opening an
Arcana Pack.

HOW TO USE (in-game):
  - Left-click and drag over cards that would be GREAT to draw right now.
    They turn GREEN.
  - Hold SHIFT, then click and drag over cards that are just OKAY.
    They turn YELLOW.
  - Drag over an already-marked card again (same mode) to clear it back to
    normal.
  - Use the Normal / Jumbo / Mega buttons at the top to match the pack size
    you're about to open.

Card data (names, images, groupings) lives in data/tarot_cards.py.
The math lives in utils/odds_calculator.py.
"""

import tkinter as tk

from tabs.base_tab import BaseTab
from data.tarot_cards import TAROT_GROUPS, get_all_cards
from data.pack_config import PACK_SIZES, DEFAULT_PACK_SIZE
from utils.odds_calculator import calculate_expected_value_percent
from utils.image_loader import load_card_image
from utils.scrollable_frame import ScrollableFrame


CARD_COLORS = {
    "none": "#2b2b40",
    "great": "#3ddc73",
    "okay": "#e8c547",
    "blocked": "#7d7d82"
}


class CardTile(tk.Frame):
    """A single clickable/drag-able tarot card box."""

    def __init__(self, parent, tab, card_name, image_filename):
        super().__init__(parent, bg=CARD_COLORS["none"], bd=2, relief="ridge",
                          width=85, height=118)
        self.tab = tab
        self.card_name = card_name
        self.state = "none"
        self.pack_propagate(False)

        self.tk_image = load_card_image(image_filename, size=(68, 68))

        self.image_label = tk.Label(self, bg=CARD_COLORS["none"])
        if self.tk_image is not None:
            self.image_label.configure(image=self.tk_image)
        else:
            self.image_label.configure(
                text="(no image set)",
                fg="#8888a0",
                font=("Segoe UI", 7, "italic"),
                wraplength=70,
            )
        self.image_label.pack(pady=(8, 3))

        self.name_label = tk.Label(
            self, text=card_name, bg=CARD_COLORS["none"], fg="white",
            font=("Segoe UI", 8, "bold"), wraplength=78, justify="center",
        )
        self.name_label.pack()

        # Bind the drag-select events to this frame AND its child labels,
        # so it doesn't matter exactly where inside the card you click.
        for widget in (self, self.image_label, self.name_label):
            widget.bind("<ButtonPress-1>", self.tab.on_drag_start)
            widget.bind("<B1-Motion>", self.tab.on_drag_motion)
            widget.bind("<ButtonRelease-1>", self.tab.on_drag_end)
            widget.card_tile = self

    def set_state(self, new_state):
        self.state = new_state
        color = CARD_COLORS[new_state]
        self.configure(bg=color)
        self.image_label.configure(bg=color)
        self.name_label.configure(bg=color)


class TarotOddsTab(BaseTab):
    TAB_ID = "tarot_odds"
    TAB_NAME = "Tarot Odds"

    def build_content(self):
        self.dragging = False
        self.drag_target_state = "great"
        self._touched_cards = set()
        self.card_tiles = []  # every CardTile we create, so we can total them up

        self.selected_pack_size = tk.StringVar(value=DEFAULT_PACK_SIZE)

        self._build_top_bar()
        self._build_card_grid()

        self.update_expected_value()

    # ---------- TOP BAR: pack size buttons + expected value display ----------

    def _build_top_bar(self):
        top_bar = tk.Frame(self.content, bg="#151521")
        top_bar.pack(fill="x", side="top", pady=(0, 10))

        instructions = tk.Label(
            top_bar,
            text="Drag = mark GREAT (green)   |   Shift+Drag = mark OKAY (yellow)",
            bg="#151521", fg="#aaaaaa", font=("Segoe UI", 9, "italic"),
        )
        instructions.pack(side="top", pady=(8, 4))

        controls = tk.Frame(top_bar, bg="#151521")
        controls.pack(pady=(0, 8))

        tk.Label(controls, text="Pack Size:", bg="#151521", fg="white",
                  font=("Segoe UI", 11)).pack(side="left", padx=(0, 8))

        for size_name in PACK_SIZES:
            btn = tk.Radiobutton(
                controls, text=size_name, value=size_name,
                variable=self.selected_pack_size,
                indicatoron=False, width=10, font=("Segoe UI", 10),
                bg="#3a3a55", fg="white", selectcolor="#50507a",
                activebackground="#50507a", activeforeground="white",
                command=self.update_expected_value,
            )
            btn.pack(side="left", padx=4)

        self.ev_label = tk.Label(
            controls, text="Expected Value: --%",
            bg="#151521", fg="#3ddc73", font=("Segoe UI", 14, "bold"),
        )
        self.ev_label.pack(side="left", padx=(30, 0))

        clear_btn = tk.Button(
            controls, text="Clear All", font=("Segoe UI", 10),
            bg="#553a3a", fg="white", relief="flat", cursor="hand2",
            command=self.clear_all_cards,
        )
        clear_btn.pack(side="left", padx=(30, 0))

    # ---------- CARD GRID ----------

    GROUPS_PER_ROW = 2
    CARDS_PER_GROUP_ROW = 4

    def _build_card_grid(self):
        scroll_area = ScrollableFrame(self.content, bg="#1f1f2e")
        scroll_area.pack(fill="both", expand=True, padx=10, pady=10)

        for group_index, group in enumerate(TAROT_GROUPS):
            grid_row = group_index // self.GROUPS_PER_ROW
            grid_col = group_index % self.GROUPS_PER_ROW

            group_block = tk.Frame(scroll_area.inner, bg="#1f1f2e")
            group_block.grid(row=grid_row, column=grid_col, sticky="nw",
                              padx=15, pady=10)

            group_label = tk.Label(
                group_block, text=group["group_name"],
                bg="#1f1f2e", fg="#e8c547", font=("Segoe UI", 13, "bold"),
                wraplength=380, justify="left",
            )
            group_label.pack(anchor="w", pady=(0, 5))

            row_frame = tk.Frame(group_block, bg="#1f1f2e")
            row_frame.pack(anchor="w")

            for i, card in enumerate(group["cards"]):
                tile = CardTile(row_frame, self, card["name"], card.get("image"))
                tile.grid(row=i // self.CARDS_PER_GROUP_ROW,
                          column=i % self.CARDS_PER_GROUP_ROW, padx=6, pady=6)
                self.card_tiles.append(tile)

    # ---------- DRAG-SELECT LOGIC ----------

    def on_drag_start(self, event):
        shift_held = (event.state & 0x0001) != 0
        ctrl_held = (event.state & 0x0004) != 0
        if ctrl_held:
            self.drag_target_state = "blocked"
        elif shift_held:
            self.drag_target_state = "okay"
        else:
            self.drag_target_state = "great"

        card_tile = self._find_card_tile(event)
        if card_tile is None:
            self.dragging = False
            return

        self.dragging = True

        if card_tile.state == self.drag_target_state:
            self.drag_target_state = "none"

        self._touched_cards = {card_tile}
        card_tile.set_state(self.drag_target_state)
        self.update_expected_value()

    def on_drag_motion(self, event):
        if not self.dragging:
            return
        card_tile = self._find_card_tile(event)
        if card_tile is None or card_tile in self._touched_cards:
            return
        self._touched_cards.add(card_tile)
        card_tile.set_state(self.drag_target_state)
        self.update_expected_value()

    def on_drag_end(self, event):
        self.dragging = False
        self._touched_cards = set()

    def _find_card_tile(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        return getattr(widget, "card_tile", None)

    # ---------- EXPECTED VALUE ----------

    def update_expected_value(self):
        great_count = sum(1 for t in self.card_tiles if t.state == "great")
        okay_count = sum(1 for t in self.card_tiles if t.state == "okay")
        blocked_count = sum(1 for t in self.card_tiles if t.state == "blocked")
        total_card_count = len(get_all_cards())

        pack_size_name = self.selected_pack_size.get()
        pack = PACK_SIZES[pack_size_name]

        ev_percent = calculate_expected_value_percent(
            great_count=great_count,
            okay_count=okay_count,
            blocked_count=blocked_count,
            total_card_count=total_card_count,
            offer_size=pack["offer"],
            use_size=pack["use"],
        )

        self.ev_label.configure(text=f"Expected Value: {ev_percent:.1f}%")

    def clear_all_cards(self):
        for tile in self.card_tiles:
            tile.set_state("none")
        self.update_expected_value()
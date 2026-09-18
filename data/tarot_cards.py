"""
TAROT CARD DATA
-----------------
Edit this file to:
  - rename tarot cards
  - move cards between groups, rename groups, or add new groups
  - point a card at your own image file

IMAGES:
  Put your image files in the assets/tarot/ folder, then set a card's
  "image" value to match the filename exactly (e.g. "the_fool.png").
  If a file is missing, the app just shows a "(no image set)" placeholder
  box instead of crashing, so you can add images gradually whenever you want.

GROUPS:
  Each group is just a label + a list of cards, and only exists to visually
  organize the reference sheet - it doesn't affect the math at all. Feel
  free to reorganize these however makes sense to you (by mechanic, by how
  often you'd use them, alphabetically, whatever).

NOTE: The groupings below are a reasonable starting guess at how the base
game's tarot cards function. Double check them against however the
Multiplayer Mod actually works and adjust as needed - that's the whole point
of this being easy to edit!
"""

TAROT_GROUPS = [
    {
        "group_name": "Enhancement Tarots (add card enhancements)",
        "cards": [
            {"name": "The Magician", "image": "the_magician.png"},      # Lucky
            {"name": "The Empress", "image": "the_empress.png"},        # Mult
            {"name": "The Hierophant", "image": "the_hierophant.png"},  # Bonus
            {"name": "The Lovers", "image": "the_lovers.png"},          # Wild
            {"name": "The Chariot", "image": "the_chariot.png"},        # Steel
            {"name": "Justice", "image": "justice.png"},                # Glass
            {"name": "The Devil", "image": "the_devil.png"},            # Gold
            {"name": "The Tower", "image": "the_tower.png"},            # Stone
        ],
    },
    {
        "group_name": "Suit Change Tarots",
        "cards": [
            {"name": "The Star", "image": "the_star.png"},   # -> Diamonds
            {"name": "The Moon", "image": "the_moon.png"},   # -> Clubs
            {"name": "The Sun", "image": "the_sun.png"},     # -> Hearts
            {"name": "The World", "image": "the_world.png"},  # -> Spades
        ],
    },
    {
        "group_name": "Rank / Level Tarots",
        "cards": [
            {"name": "Strength", "image": "strength.png"},
            {"name": "The High Priestess", "image": "the_high_priestess.png"},
            {"name": "The Emperor", "image": "the_emperor.png"},
            {"name": "The Wheel of Fortune", "image": "the_wheel_of_fortune.png"},
        ],
    },
    {
        "group_name": "Money Tarots",
        "cards": [
            {"name": "The Hermit", "image": "the_hermit.png"},
            {"name": "Temperance", "image": "temperance.png"},
        ],
    },
    {
        "group_name": "Destroy / Create / Copy Tarots",
        "cards": [
            {"name": "The Fool", "image": "the_fool.png"},
            {"name": "The Hanged Man", "image": "the_hanged_man.png"},
            {"name": "Death", "image": "death.png"},
            {"name": "Judgement", "image": "judgement.png"},
        ],
    },
]


def get_all_cards():
    """Returns one flat list of every card (used to count the total pool size)."""
    all_cards = []
    for group in TAROT_GROUPS:
        all_cards.extend(group["cards"])
    return all_cards
"""
This file is the master list of every reference-sheet tab in the app.

TO ADD A NEW TAB:
  1. Import your new tab class at the top of this file.
  2. Add it to the ALL_TABS list below.
  3. Save - it will automatically appear as a button on the home screen.

TO REMOVE OR HIDE A TAB:
  Just delete or comment out its line in ALL_TABS below.
"""

from tabs.tarot_odds import TarotOddsTab

ALL_TABS = [
    TarotOddsTab,
    # Add future tabs here, for example:
    # from tabs.planet_odds import PlanetOddsTab
    # PlanetOddsTab,
]
"""
ODDS CALCULATOR
------------------
This file does the math behind the "expected value" percentage shown on the
Tarot Odds tab. It has no tkinter/GUI code in it at all, so you can test or
tweak the math here without worrying about breaking the window.

THE IDEA:
  - You mark some tarot cards as "Great" (worth 1 full point if you use them)
  - You mark some tarot cards as "Okay" (worth 0.5 points if you use them)
  - Every other tarot card is worth 0 points.
  - An Arcana Pack shows you `offer_size` random cards (no repeats) out of
    every tarot card that exists in the game, and lets you use `use_size`
    of them.
  - We assume you play smart: if a Great card shows up, you use it; if
    there's still a free "use" slot left, you fill it with an Okay card.
  - The "expected value" is the average number of points you'd walk away
    with, shown as a percentage of the best possible outcome (using nothing
    but Great cards).
"""

from math import comb


def calculate_expected_value_percent(great_count, okay_count, total_card_count,
                                      offer_size, use_size):
    """
    great_count      -> how many cards are currently marked "Great"
    okay_count       -> how many cards are currently marked "Okay"
    total_card_count -> how many tarot cards exist in total (the whole pool)
    offer_size       -> how many cards the pack shows you
    use_size         -> how many of those cards you're allowed to use

    Returns a number from 0 to 100 (a percentage).
    """

    other_count = total_card_count - great_count - okay_count

    # Safety checks so the program never crashes from odd inputs.
    if total_card_count <= 0 or offer_size <= 0 or use_size <= 0:
        return 0.0
    if other_count < 0:
        other_count = 0

    ways_to_draw_offer = comb(total_card_count, offer_size)
    if ways_to_draw_offer == 0:
        return 0.0

    total_points = 0.0  # builds up the average ("expected") points

    max_great_in_offer = min(great_count, offer_size)

    # Try every possible combination of (great cards drawn, okay cards drawn)
    # that could appear among the offered cards, weighted by how likely
    # each combination is.
    for great_drawn in range(0, max_great_in_offer + 1):
        max_okay_in_offer = min(okay_count, offer_size - great_drawn)

        for okay_drawn in range(0, max_okay_in_offer + 1):
            other_drawn = offer_size - great_drawn - okay_drawn

            if other_drawn < 0 or other_drawn > other_count:
                continue  # not a possible combination

            ways_this_combo = (
                comb(great_count, great_drawn)
                * comb(okay_count, okay_drawn)
                * comb(other_count, other_drawn)
            )
            if ways_this_combo == 0:
                continue

            probability_of_this_combo = ways_this_combo / ways_to_draw_offer

            # Use Great cards first, then fill remaining slots with Okay cards.
            great_used = min(great_drawn, use_size)
            remaining_use_slots = use_size - great_used
            okay_used = min(okay_drawn, remaining_use_slots)

            points_from_this_combo = (great_used * 1.0) + (okay_used * 0.5)

            total_points += probability_of_this_combo * points_from_this_combo

    best_possible_points = use_size * 1.0
    expected_value_percent = (total_points / best_possible_points) * 100

    return expected_value_percent
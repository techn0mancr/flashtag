"""
Definitions of global constants pertaining to general configuration.

Written by techn0mancr.
"""

# Custom library imports
from helper import path_join

BASE_DIR = {
    "deck": path_join("decks"),
    "font": path_join("fonts")
}

FONT = {
    "small": {
        "line_spacing": 0.75,
        "text_font": path_join(BASE_DIR["font"], "Bookerly-Regular-12.pcf"),
        "text_length_range": range(225, 375),
        "text_wrap": 48
    },
    "medium": {
        "line_spacing": 0.75,
        "text_font": path_join(BASE_DIR["font"], "Bookerly-Regular-16.pcf"),
        "text_length_range": range(75, 225),
        "text_wrap": 35
    },
    "large": {
        "line_spacing": 0.75,  # formerly 1.0
        "text_font": path_join(BASE_DIR["font"], "Bookerly-Regular-20.pcf"),
        "text_length_range": range(0, 75),
        "text_wrap": 30
    }
}

POSITION_VECTOR = {
    "center": (0.5, 0.5)
}
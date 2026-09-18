"""
IMAGE LOADER
--------------
Small helper for loading card images.

If Pillow (PIL) is installed, it's used automatically so images can be
resized and more file types are supported. If Pillow is NOT installed, only
.png/.gif/.pgm/.ppm files can be loaded, and they won't be resized - that's
fine, the app still works either way.

If an image can't be found or can't be loaded, this returns None, and the
card just shows a text placeholder instead of crashing.
"""

import os
import tkinter as tk

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

ASSETS_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "tarot",
)

# Keep references to loaded images so Python's garbage collector doesn't
# delete them while they're still being displayed on screen.
_image_cache = {}


def load_card_image(filename, size=(90, 90)):
    if not filename:
        return None

    path = os.path.join(ASSETS_FOLDER, filename)
    if not os.path.exists(path):
        return None

    cache_key = (path, size)
    if cache_key in _image_cache:
        return _image_cache[cache_key]

    try:
        if PIL_AVAILABLE:
            pil_image = Image.open(path)
            pil_image = pil_image.resize(size)
            tk_image = ImageTk.PhotoImage(pil_image)
        else:
            tk_image = tk.PhotoImage(file=path)
    except Exception:
        return None

    _image_cache[cache_key] = tk_image
    return tk_image
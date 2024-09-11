from .window import create_window
from .widgets import add_button, add_slider, add_text

__version__ = "1.0"

def create_djungarik_window(title="Djungarik", width=300, height=300):
    window = create_window(title, width, height)
    return window

__all__ = ['create_djungarik_window', 'add_button', 'add_slider', 'add_text']

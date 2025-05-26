"""
The home page
"""
import dash
dash.register_page("home", layout="We're home!", path="/")
from pages.home.layout import get_layout
layout = get_layout()
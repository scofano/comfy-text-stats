# __init__.py
from .text_stats import TextStats

# ComfyUI looks for these two mappings:
NODE_CLASS_MAPPINGS = {
    "TextStats": TextStats,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextStats": "Text → Char & Word Count",
}

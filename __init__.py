"""ComfyUI node registration for comfy-text-stats."""

from .line_context_counter import LineContextCounter
from .text_stats import TextStats
from .utf8_processor import UTF8Processor

NODE_CLASS_MAPPINGS = {
    "LineContextCounter": LineContextCounter,
    "TextStats": TextStats,
    "UTF8Processor": UTF8Processor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LineContextCounter": "Text → Line Context Counter",
    "TextStats": "Text → Char, Word & Line Count",
    "UTF8Processor": "Text → UTF-8 Cleaner",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "LineContextCounter",
    "TextStats",
    "UTF8Processor",
]

__version__ = "1.4.1"

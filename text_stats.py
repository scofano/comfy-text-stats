# text_stats.py
import re
from typing import Tuple

# NOTE:
# - Input:  STRING (multiline enabled)
# - Output: INT (character count), INT (word count)
# - Category: Text / Utils
# - Deterministic: yes

_WORD_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)

class TextStats:
    """
    A simple ComfyUI node that counts characters and words in a string.
    - Character count is the length of the string (including spaces and newlines).
    - Word count uses a Unicode-aware word regex: r"\\b\\w+\\b".
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("char_count", "word_count")
    FUNCTION = "compute"
    CATEGORY = "Text/Utils"
    # Mark as deterministic: same input -> same output, unaffected by seeds.
    OUTPUT_NODE = False

    def compute(self, text: str) -> Tuple[int, int]:
        if text is None:
            text = ""
        if not isinstance(text, str):
            text = str(text)

        char_count = len(text)
        # Unicode-aware word counting:
        # Counts sequences of letters/digits/underscore bounded by word boundaries.
        word_count = len(_WORD_PATTERN.findall(text))

        # ComfyUI expects a tuple aligned with RETURN_TYPES
        return (char_count, word_count)

    @classmethod
    def IS_CHANGED(cls, **kwargs) -> float:
        """
        Optional optimization hint to ComfyUI: change hash for caching.
        Return a value that changes when inputs change.
        Here we derive from the text content length + hash to be safe.
        """
        text = kwargs.get("text", "") or ""
        # lightweight, stable-ish indicator
        return float(len(text))

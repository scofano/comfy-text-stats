from typing import Tuple


def _truncate_string(string: str, max_length: int, mode: str = "end", truncate_by: str = "characters") -> str:
    """
    Truncate *string* to *max_length* units (characters or words).

    Args:
        string:      The input text to truncate.
        max_length:  Positive -> keep that many units from the selected side.
                     Negative -> use Python-style slicing from the selected side.
        mode:        ``"beginning"`` -> keep from the beginning of the text.
                     ``"end"``       -> keep from the end of the text.
        truncate_by: ``"characters"`` or ``"words"``.

    Returns:
        The truncated string.
    """
    if not isinstance(string, str):
        string = str(string)

    if mode not in ("beginning", "end"):
        mode = "end"
    if truncate_by not in ("characters", "words"):
        truncate_by = "characters"
    max_length = int(max_length)

    if max_length == 0:
        return ""

    if truncate_by == "characters":
        if mode == "beginning":
            # Keep from the beginning of the string.
            return string[:max_length] if max_length >= 0 else string[max_length:]
        # Keep from the end of the string.
        return string[-max_length:] if max_length >= 0 else string[:max_length]

    # --- word-level truncation ---
    # Split on whitespace like the original script
    words = string.split()
    if not words:
        return ""

    if mode == "beginning":
        return " ".join(words[:max_length]) if max_length >= 0 else " ".join(words[max_length:])
    # mode == "end"
    return " ".join(words[-max_length:]) if max_length >= 0 else " ".join(words[:max_length])


class TextStringTruncate:
    """
    ComfyUI node that truncates a text string.

    Inputs:
      - text:         The input string (multiline).
      - truncate_to:  The target length (positive or negative integer).
      - truncate_by:  ``"characters"`` or ``"words"``.
      - truncate_from: ``"beginning"`` (slice from the beginning) or
                       ``"end"`` (slice from the end).

    Output:
      - text: The truncated string.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "truncate_to": ("INT", {"default": 10, "min": -999999, "max": 999999}),
                "truncate_by": (("characters", "words"), {"default": "characters"}),
                "truncate_from": (("end", "beginning"), {"default": "end"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "truncate"
    CATEGORY = "Text/Utils"
    OUTPUT_NODE = False

    def truncate(
        self,
        text: str,
        truncate_to: int,
        truncate_by: str,
        truncate_from: str,
    ) -> Tuple[str]:
        result = _truncate_string(
            string=text,
            max_length=truncate_to,
            mode=truncate_from,
            truncate_by=truncate_by,
        )
        return (result,)

    @classmethod
    def IS_CHANGED(cls, **kwargs) -> str:
        text = kwargs.get("text", "") or ""
        truncate_to = int(kwargs.get("truncate_to", 10) or 0)
        truncate_by = kwargs.get("truncate_by", "characters") or "characters"
        truncate_from = kwargs.get("truncate_from", "end") or "end"
        return f"{len(text)}:{truncate_to}:{truncate_by}:{truncate_from}"
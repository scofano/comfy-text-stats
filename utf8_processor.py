# utf8_processor.py
import unicodedata
from typing import Tuple

# Common typography/invisible-character cleanup while preserving valid Unicode
# letters such as á, é, í, ó, ú, ç, etc.
_CHAR_REPLACEMENTS = str.maketrans(
    {
        ord("…"): "...",
        ord("–"): "-",
        ord("—"): "-",
        ord("−"): "-",
        ord("‐"): "-",
        ord("‑"): "-",
        ord("“"): '"',
        ord("”"): '"',
        ord("„"): '"',
        ord("«"): '"',
        ord("»"): '"',
        ord("‘"): "'",
        ord("’"): "'",
        ord("‚"): "'",
        ord("´"): "'",
        ord("`"): "'",
        ord("•"): "-",
        ord("·"): "-",
        ord("→"): "->",
        ord("←"): "<-",
        ord("↔"): "<->",
        ord("⇒"): "=>",
        ord("⇐"): "<=",
        ord("⇔"): "<=>",
        ord("\u00A0"): " ",
        ord("\u202F"): " ",
        ord("\u2007"): " ",
        ord("\u2009"): " ",
        ord("\u200B"): "",
        ord("\u200C"): "",
        ord("\u200D"): "",
        ord("\u2060"): "",
        ord("\uFEFF"): "",
        ord("\u00AD"): "",
    }
)

_ALLOWED_WHITESPACE = {"\n", "\t"}


def _clean_utf8_text(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.translate(_CHAR_REPLACEMENTS)

    # Drop any invalid surrogate data while keeping valid UTF-8/Unicode text.
    utf8_safe = normalized.encode("utf-8", errors="ignore").decode("utf-8")

    cleaned_chars = []
    for char in utf8_safe:
        if char in _ALLOWED_WHITESPACE:
            cleaned_chars.append(char)
            continue

        # Remove control/format/private-use/surrogate chars, keep visible Unicode.
        if unicodedata.category(char).startswith("C"):
            continue

        cleaned_chars.append(char)

    return "".join(cleaned_chars)


class UTF8Processor:
    """
    Cleans text into a UTF-8-safe string while preserving valid Unicode letters.
    Replaces common smart punctuation with simpler equivalents and removes
    invisible/control characters. Also normalizes common arrow symbols to
    ASCII equivalents and converts common non-breaking/thin spaces to regular
    spaces so downstream Windows charmap encoders are less likely to fail.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("clean_text",)
    FUNCTION = "process"
    CATEGORY = "Text/Utils"
    OUTPUT_NODE = False

    def process(self, text: str) -> Tuple[str]:
        if text is None:
            text = ""
        if not isinstance(text, str):
            text = str(text)

        return (_clean_utf8_text(text),)

    @classmethod
    def IS_CHANGED(cls, **kwargs) -> float:
        text = kwargs.get("text", "") or ""
        return float(len(text))
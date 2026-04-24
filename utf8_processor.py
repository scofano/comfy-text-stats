# utf8_processor.py
import locale
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

_ENCODING_FALLBACKS = {
    "ß": "ss",
    "ẞ": "SS",
    "æ": "ae",
    "Æ": "AE",
    "œ": "oe",
    "Œ": "OE",
    "ø": "o",
    "Ø": "O",
    "ð": "d",
    "Ð": "D",
    "þ": "th",
    "Þ": "TH",
    "ł": "l",
    "Ł": "L",
    "đ": "d",
    "Đ": "D",
    "ı": "i",
    "Ĳ": "IJ",
    "ĳ": "ij",
}


def _can_encode(text: str, encoding: str) -> bool:
    try:
        text.encode(encoding)
        return True
    except UnicodeEncodeError:
        return False


def _transliterate_for_encoding(char: str, encoding: str) -> str:
    direct_fallback = _ENCODING_FALLBACKS.get(char)
    if direct_fallback and _can_encode(direct_fallback, encoding):
        return direct_fallback

    # Decompose accented characters (e.g. ă -> a + combining breve), then
    # drop the combining marks so Windows non-UTF-8 code pages can still
    # encode the nearest readable equivalent.
    decomposed = unicodedata.normalize("NFKD", char)
    stripped = "".join(part for part in decomposed if not unicodedata.combining(part))

    if stripped and _can_encode(stripped, encoding):
        return stripped

    return ""


def _coerce_to_preferred_encoding(text: str) -> str:
    preferred_encoding = locale.getpreferredencoding(False) or "utf-8"

    if preferred_encoding.lower().replace("-", "") == "utf8":
        return text

    if _can_encode(text, preferred_encoding):
        return text

    safe_chars = []
    for char in text:
        if char in _ALLOWED_WHITESPACE:
            safe_chars.append(char)
            continue

        if _can_encode(char, preferred_encoding):
            safe_chars.append(char)
            continue

        safe_chars.append(_transliterate_for_encoding(char, preferred_encoding))

    return "".join(safe_chars)


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

    cleaned_text = "".join(cleaned_chars)
    return _coerce_to_preferred_encoding(cleaned_text)


class UTF8Processor:
    """
    Cleans text into a UTF-8-safe string while preserving valid Unicode letters.
    Replaces common smart punctuation with simpler equivalents and removes
    invisible/control characters. Also normalizes common arrow symbols to
    ASCII equivalents and converts common non-breaking/thin spaces to regular
    spaces. On systems whose default text encoding is not UTF-8 (common on
    Windows), unsupported characters are transliterated to the closest
    encodable equivalent so downstream charmap writes do not fail.
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
# character_search_replace.py
from typing import List, Tuple


DEFAULT_REPLACEMENTS = (
    "“|\"\n"
    "”|\"\n"
    "„|\"\n"
    "«|\"\n"
    "»|\"\n"
    "‘|'\n"
    "’|'\n"
    "‚|'\n"
    "´|'\n"
    "`|'\n"
    "–|-\n"
    "—|, \n"
    "−|-\n"
    "‐|-\n"
    "‑|-\n"
    "•|-\n"
    "·|-\n"
    "*|\n"
    " |_\n"
    "…|..."
)


def _parse_replacement_rules(replacements: str) -> List[Tuple[str, str]]:
    rules: List[Tuple[str, str]] = []

    for line in replacements.splitlines():
        if not line:
            continue
        if "|" not in line:
            continue
        search, replace = line.split("|", 1)
        if search:
            rules.append((search, replace))

    return rules


def _replace_characters(text: str, replacements: str) -> str:
    result = text

    for search, replace in _parse_replacement_rules(replacements):
        result = result.replace(search, replace)

    return result


class CharacterSearchReplace:
    """
    Replaces strings using a multiline mapping list.

    Each non-empty line defines one rule using a `|` separator:
      search_string|replacement_string

    Everything before the first `|` is the search target (may be multiple
    characters). Everything after is the replacement (may be empty, to delete).
    Lines without `|` are silently skipped.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "replacements": (
                    "STRING",
                    {"multiline": True, "default": DEFAULT_REPLACEMENTS},
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "process"
    CATEGORY = "Text/Utils"
    OUTPUT_NODE = False

    def process(self, text: str, replacements: str) -> Tuple[str]:
        if text is None:
            text = ""
        if not isinstance(text, str):
            text = str(text)

        if replacements is None:
            replacements = ""
        if not isinstance(replacements, str):
            replacements = str(replacements)

        return (_replace_characters(text, replacements),)

    @classmethod
    def IS_CHANGED(cls, **kwargs) -> float:
        text = kwargs.get("text", "") or ""
        replacements = kwargs.get("replacements", "") or ""
        return float(len(text) + len(replacements))

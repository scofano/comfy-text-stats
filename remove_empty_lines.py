from typing import Tuple


def _remove_empty_lines(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if line.strip())


class RemoveEmptyLines:
    """Removes empty or whitespace-only lines from a multiline string."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "process"
    CATEGORY = "Text/Utils"
    OUTPUT_NODE = False

    def process(self, text: str) -> Tuple[str]:
        if text is None:
            text = ""
        if not isinstance(text, str):
            text = str(text)

        return (_remove_empty_lines(text),)

    @classmethod
    def IS_CHANGED(cls, **kwargs) -> float:
        text = kwargs.get("text", "") or ""
        return float(len(text))
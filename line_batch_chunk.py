from typing import Tuple


def _get_line_batch(text: str, number_of_lines: int, batch: int) -> str:
    lines = text.splitlines()

    start_index = (batch - 1) * number_of_lines
    end_index = start_index + number_of_lines

    if start_index >= len(lines):
        return ""

    return "\n".join(lines[start_index:end_index])


class LineBatchChunk:
    """Returns a batch-sized chunk from a multiline string."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "number_of_lines": ("INT", {"default": 2, "min": 1, "step": 1}),
                "batch": (
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "step": 1,
                        "control_after_generate": "increment",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("chunk_text",)
    FUNCTION = "process"
    CATEGORY = "Text/Utils"
    OUTPUT_NODE = False

    def process(self, text: str, number_of_lines: int, batch: int) -> Tuple[str]:
        if text is None:
            text = ""
        if not isinstance(text, str):
            text = str(text)

        number_of_lines = max(1, int(number_of_lines))
        batch = max(1, int(batch))

        return (_get_line_batch(text, number_of_lines, batch),)

    @classmethod
    def IS_CHANGED(cls, **kwargs) -> float:
        text = kwargs.get("text", "") or ""
        number_of_lines = max(1, int(kwargs.get("number_of_lines", 1) or 1))
        batch = max(1, int(kwargs.get("batch", 1) or 1))
        return float(len(text) + number_of_lines + batch)
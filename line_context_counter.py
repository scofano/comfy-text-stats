from typing import Tuple


class _SafeFormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def _render_output(prefix: str, content: str, **values: str) -> str:
    if not content:
        return ""

    prefix = prefix or ""
    if not prefix:
        return content

    if "{" in prefix and "}" in prefix:
        format_values = _SafeFormatDict(values)
        return prefix.format_map(format_values)

    return f"{prefix}{content}"


def _join_non_empty_lines(*parts: str) -> str:
    return "\n".join(part for part in parts if part)


class LineContextCounter:
    """
    Iterates through a multiline string using a visible counter input and
    exposes the current line plus configurable previous/next line context.

    The counter starts at line 1 and is configured to auto-increment after
    each execution in the ComfyUI widget, similar to a seed field.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "set_counter": (
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "step": 1,
                        "control_after_generate": "increment",
                    },
                ),
                "previous_lines": ("INT", {"default": 1, "min": 0, "step": 1}),
                "next_lines": ("INT", {"default": 1, "min": 0, "step": 1}),
                "current_prefix": (
                    "STRING",
                    {"default": "Current line: {line}", "multiline": False},
                ),
                "previous_prefix": (
                    "STRING",
                    {"default": "Previous {count} lines: {lines}", "multiline": False},
                ),
                "next_prefix": (
                    "STRING",
                    {"default": "Next {count} lines: {lines}", "multiline": False},
                ),
                "all_lines_prefix": (
                    "STRING",
                    {"default": "All the content: ", "multiline": False},
                ),
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "counter",
        "current_line_text",
        "previous_lines_text",
        "next_lines_text",
        "combined_context_text",
        "all_lines_text",
    )
    FUNCTION = "process"
    CATEGORY = "Text/Utils"
    OUTPUT_NODE = False

    def process(
        self,
        text: str,
        set_counter: int,
        previous_lines: int,
        next_lines: int,
        current_prefix: str,
        previous_prefix: str,
        next_prefix: str,
        all_lines_prefix: str,
    ) -> Tuple[int, str, str, str, str, str]:
        if text is None:
            text = ""
        if not isinstance(text, str):
            text = str(text)

        lines = text.splitlines()

        if not lines:
            return (0, "", "", "", "", "")

        set_counter = max(1, int(set_counter))
        previous_lines = max(0, int(previous_lines))
        next_lines = max(0, int(next_lines))

        current_index = (set_counter - 1) % len(lines)
        current_line_number = current_index + 1

        current_line = lines[current_index]
        previous_chunk = "\n".join(lines[max(0, current_index - previous_lines):current_index])
        next_chunk = "\n".join(lines[current_index + 1:current_index + 1 + next_lines])
        all_lines_text = _render_output(
            all_lines_prefix,
            text,
            line=text,
            lines=text,
            count=str(len(lines)),
            actual_count=str(len(lines)),
            line_number=str(current_line_number),
            total_lines=str(len(lines)),
        )

        current_line_text = _render_output(
            current_prefix,
            current_line,
            line=current_line,
            lines=current_line,
            count="1",
            actual_count="1",
            line_number=str(current_line_number),
            total_lines=str(len(lines)),
        )

        previous_lines_text = _render_output(
            previous_prefix,
            previous_chunk,
            line=previous_chunk,
            lines=previous_chunk,
            count=str(previous_lines),
            actual_count=str(len(previous_chunk.splitlines()) if previous_chunk else 0),
            line_number=str(current_line_number),
            total_lines=str(len(lines)),
        )

        next_lines_text = _render_output(
            next_prefix,
            next_chunk,
            line=next_chunk,
            lines=next_chunk,
            count=str(next_lines),
            actual_count=str(len(next_chunk.splitlines()) if next_chunk else 0),
            line_number=str(current_line_number),
            total_lines=str(len(lines)),
        )

        combined_context_text = _join_non_empty_lines(
            previous_lines_text,
            current_line_text,
            next_lines_text,
        )

        return (
            current_line_number,
            current_line_text,
            previous_lines_text,
            next_lines_text,
            combined_context_text,
            all_lines_text,
        )

    @classmethod
    def IS_CHANGED(cls, **kwargs) -> float:
        text = kwargs.get("text", "") or ""
        set_counter = max(1, int(kwargs.get("set_counter", 1) or 1))
        return float(len(text) + set_counter)
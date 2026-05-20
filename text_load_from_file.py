import io
import os
from typing import Dict, List, Tuple


def _filename_key(file_path: str, dictionary_name: str = "[filename]") -> str:
    """Return the output dictionary key, matching the WAS Text Load behavior."""
    basename = os.path.basename(file_path)
    filename = basename.split(".", 1)[0] if "." in basename else basename
    return dictionary_name if dictionary_name != "[filename]" else filename


def _load_text_file(file_path: str, dictionary_name: str = "[filename]") -> Tuple[str, Dict[str, List[str]]]:
    """
    Load a UTF-8 text file, skipping comment lines.

    Lines whose stripped content starts with ``#`` are excluded. Returned lines
    have ``\n`` and ``\r`` removed, then are joined with ``\n`` for the text
    output and included as a list in the dictionary output.
    """
    key = _filename_key(file_path, dictionary_name)

    if not os.path.exists(file_path):
        print(f"[Text Load From File] The path `{file_path}` specified cannot be found.")
        return "", {key: []}

    with open(file_path, "r", encoding="utf-8", newline="\n") as file:
        text = file.read()

    lines = []
    for line in io.StringIO(text):
        if not line.strip().startswith("#"):
            lines.append(line.replace("\n", "").replace("\r", ""))

    return "\n".join(lines), {key: lines}


class TextLoadFromFile:
    """Load text from a UTF-8 file and return both joined text and a line dictionary."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "", "multiline": False}),
                "dictionary_name": ("STRING", {"default": "[filename]", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING", "DICT")
    RETURN_NAMES = ("text", "dictionary")
    FUNCTION = "load_file"
    CATEGORY = "Text/Utils"
    OUTPUT_NODE = False

    def load_file(self, file_path: str = "", dictionary_name: str = "[filename]") -> Tuple[str, Dict[str, List[str]]]:
        if file_path is None:
            file_path = ""
        if dictionary_name is None:
            dictionary_name = "[filename]"

        return _load_text_file(str(file_path), str(dictionary_name))

    @classmethod
    def IS_CHANGED(cls, **kwargs) -> str:
        file_path = str(kwargs.get("file_path", "") or "")
        dictionary_name = str(kwargs.get("dictionary_name", "[filename]") or "[filename]")

        if not os.path.exists(file_path):
            return f"missing:{file_path}:{dictionary_name}"

        try:
            stat = os.stat(file_path)
            return f"{file_path}:{dictionary_name}:{stat.st_mtime_ns}:{stat.st_size}"
        except OSError:
            return f"error:{file_path}:{dictionary_name}"
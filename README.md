# 🧩 Comfy Text Stats

A lightweight **ComfyUI custom node pack** with text utility nodes for working directly inside your workflows:

- 🔁 **Line Context Counter** — uses a visible counter that auto-increments like a seed and returns the current, previous, and next line context
- 🧮 **Text Stats** — returns character, word, and line counts
- 🧼 **UTF-8 Cleaner** — normalizes punctuation and removes invisible/control characters while preserving valid Unicode text

This pack is useful for text preprocessing, caption analytics, prompt inspection, and quick metadata generation directly in ComfyUI.

---

## 🚀 Features

✅ Simple and fast — no external dependencies  
✅ Unicode-aware word detection (supports multilingual text)  
✅ Line counting for multiline inputs  
✅ Sequential line traversal with previous/next context windows  
✅ Visible line counter with seed-like auto-increment and manual reset control  
✅ UTF-8-safe text cleanup with smart punctuation normalization  
✅ Deterministic utility nodes for stats and cleanup  
✅ Works with any `STRING` input from other nodes  

<p align="center">
  <img src="https://raw.githubusercontent.com/scofano/comfy-text-stats/main/text_stats.png" alt="Text stats" style="width: 100%; height: auto;">
</p>

---

## 📦 Installation

### **Option 1 — Via ComfyUI-Manager (recommended)**

1. Open **ComfyUI-Manager**
2. Search for **Comfy Text Stats**
3. Install the node pack
4. Reload custom nodes or restart ComfyUI

### **Option 2 — Manual Install**

1. Clone or download this repository into your ComfyUI custom node directory:
   ```bash
   git clone https://github.com/scofano/comfy-text-stats.git
   ```
2. The final structure should look like this:
   ```
   ComfyUI/
   └── custom_nodes/
       └── comfy-text-stats/
           ├── __init__.py
           ├── line_context_counter.py
           ├── text_stats.py
           ├── utf8_processor.py
           ├── README.md
           └── requirements.txt
   ```
3. Restart ComfyUI.

---

## 🧠 Usage

### 1) Line Context Counter
Category: `Text/Utils`

### Inputs
| Name | Type | Description |
|------|------|--------------|
| `text` | STRING | Multiline text to iterate through. |
| `set_counter` | INT | Visible line counter. Starts at `1`, auto-increments after each run like a seed, and can be changed manually at any time. |
| `previous_lines` | INT | Number of previous lines to include. Default: `1`. |
| `next_lines` | INT | Number of next lines to include. Default: `1`. |
| `current_prefix` | STRING | Optional prefix/template for the current line output. Default: `Current line: {line}` |
| `previous_prefix` | STRING | Optional prefix/template for the previous lines output. Default: `Previous {count} lines: {lines}` |
| `next_prefix` | STRING | Optional prefix/template for the next lines output. Default: `Next {count} lines: {lines}` |
| `all_lines_prefix` | STRING | Optional prefix/template for the full text output. Default: `All the content: ` |

### Outputs
| Name | Type | Description |
|------|------|--------------|
| `counter` | INT | The visible current line counter, starting at `1`. |
| `current_line_text` | STRING | The current line selected by the automatic counter, starting at line 1. |
| `previous_lines_text` | STRING | Up to the requested number of lines before the current line. Empty if none exist. |
| `next_lines_text` | STRING | Up to the requested number of lines after the current line. Empty if none exist. |
| `combined_context_text` | STRING | Previous, current, and next outputs concatenated together in that order, separated by newlines. Empty parts are skipped. |
| `all_lines_text` | STRING | The original input text with the optional all-lines prefix applied. |

Notes:
- `set_counter` behaves like a seed-style control and defaults to the `increment` post-generate mode in ComfyUI.
- The `counter` output lets you see which line is currently selected.
- You can edit `set_counter` manually at any time to jump to or reset the current line.
- If `set_counter` is larger than the number of lines, it wraps around using the available line count.
- `combined_context_text` joins `previous_lines_text`, `current_line_text`, and `next_lines_text` using newline separators.
- If `previous_lines = 0`, `previous_lines_text` is always an empty string.
- If `next_lines = 0`, `next_lines_text` is always an empty string.
- Prefix fields are optional; if left blank, the node outputs only the line content.
- Templates can use placeholders such as `{line}`, `{lines}`, `{count}`, `{actual_count}`, `{line_number}`, and `{total_lines}`.
- If there are no previous lines or no next lines available, that output is an empty string.
- If the input text is empty, the node returns `counter = 0` and empty string outputs.

### 2) Text Stats
Category: `Text/Utils`

### Inputs
| Name | Type | Description |
|------|------|--------------|
| `text` | STRING | The text input to analyze. Supports multiline input. |

### Outputs
| Name | Type | Description |
|------|------|--------------|
| `char_count` | INT | Number of characters (including spaces, punctuation, and newlines). |
| `word_count` | INT | Number of words (using Unicode-aware regex). |
| `line_count` | INT | Number of lines in the input text. |

### 3) UTF-8 Cleaner
Category: `Text/Utils`

### Inputs
| Name | Type | Description |
|------|------|--------------|
| `text` | STRING | The raw text input to sanitize. Supports multiline input. |

### Outputs
| Name | Type | Description |
|------|------|--------------|
| `clean_text` | STRING | Cleaned UTF-8-safe text with common smart punctuation normalized and invisible/control characters removed. |

---

## 🧪 Example

**Line Context Counter input:**
```text
alpha
beta
gamma
delta
```

**Run 1 outputs (defaults, `set_counter = 1`, `previous_lines = 1`, `next_lines = 1`):**
```text
counter = 1
current_line_text = Current line: alpha
previous_lines_text = 
next_lines_text = Next 1 lines: beta
combined_context_text = Current line: alpha
Next 1 lines: beta
all_lines_text = All the content: alpha
beta
gamma
delta
```

**Run 2 outputs:**
```text
counter = 2
current_line_text = Current line: beta
previous_lines_text = Previous 1 lines: alpha
next_lines_text = Next 1 lines: gamma
combined_context_text = Previous 1 lines: alpha
Current line: beta
Next 1 lines: gamma
```

**Manual reset example (`set_counter = 4`):**
```text
counter = 4
current_line_text = Current line: delta
previous_lines_text = Previous 1 lines: gamma
next_lines_text = 
```

**Zero-window examples:**
```text
previous_lines = 0  -> previous_lines_text = ""
next_lines = 0      -> next_lines_text = ""
```

**Out-of-range counter example (`set_counter = 6` on 4 lines):**
```text
counter = 2
current_line_text = Current line: beta
previous_lines_text = Previous 1 lines: alpha
next_lines_text = Next 1 lines: gamma
```

**Text Stats input:**
```
ComfyUI makes custom nodes easy!
```

**Text Stats outputs:**
```
char_count = 32
word_count = 5
line_count = 1
```

**UTF-8 Cleaner example:**
```text
Olá… mundo – teste\u200B
```

becomes:

```text
Olá... mundo - teste
```

---

## 🔧 Technical Details

- Word detection uses the regex:  
  ```python
  \b\w+\b
  ```
  which matches Unicode word boundaries.
- `LineContextCounter` uses a seed-like `set_counter` widget with `control_after_generate = "increment"`, so the counter updates automatically after each run in ComfyUI.
- `LineContextCounter` selection is driven by the current input counter value and wraps around when the counter exceeds the available line count.
- UTF-8 Cleaner normalizes text to Unicode NFC, replaces common smart punctuation (such as `…` → `...` and `–`/`—` → `-`), removes invisible/control characters, and preserves valid Unicode characters such as `áéíóúç`.
- `TextStats` counts lines using `splitlines()`, so an empty string returns `0` lines.
- `TextStats` and `UTF8Processor` are deterministic, and their `IS_CHANGED` implementations currently use input length as a lightweight cache hint.

---

## 💡 Use Cases

- Text preprocessing for captioning or prompt tuning  
- Generating text metadata before feeding into LLM pipelines  
- Measuring caption sizes in dataset workflows  
- Cleaning copy/pasted text before saving or reusing it in prompts  
- Stepping through caption or subtitle files one line at a time with surrounding context  

---

## 📄 License

MIT License © 2025 — freely usable and modifiable.  
Contributions welcome!

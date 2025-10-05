# Comfy Text Stats Node

A tiny ComfyUI custom node that takes a string and outputs **Character count** and **Word count** (both `INT`).

## What it does

- **Character count**: `len(text)` — includes spaces, punctuation, and newlines.
- **Word count**: Unicode-aware `\b\w+\b` regex.

## Install

1. Navigate to your ComfyUI installation:

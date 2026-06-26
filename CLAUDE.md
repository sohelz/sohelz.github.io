# soheilzarrinpour.com — Claude Instructions

**First action on every site task: read `core.md`.**
It is the single authoritative reference for all schemas, commands, conventions, and the trash system.

## Critical Rules

- Never edit generated HTML files. Always edit source files in `_content/` or `_templates/`, then run `python3 build.py`.
- Never permanently delete content. Move removed files to `_trash/posts/` or `_trash/pages/`. See core.md → TRASH SYSTEM.
- After every change: `python3 build.py && git add . && git commit -m "..." && git push`

## Consultation Syntax

Text the user wraps in `#` characters (e.g. `#note to Claude#`) is a private instruction. Strip it from all published content.

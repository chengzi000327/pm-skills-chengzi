---
name: browser-use
description: Perform browser automation tasks - navigate websites, fill forms, scrape data, take screenshots, and automate web workflows. Use when asked to browse, search, interact with websites, or automate web tasks.
---

# Browser Use

A wrapper around the browser-use library that enables Claude Code to perform browser automation through two modes.

## Triggers

Use this skill when the user says:
- "browse to...", "open website..."
- "search for...", "find on web..."
- "fill out form...", "automate..."
- "web research...", "scrape..."
- "take screenshot of..."

## Setup (First Time)

```bash
pip install browser-use
playwright install chromium
cp -r ~/.claude/skills/browser-use ~/.claude/skills/browser-use-skill
cd ~/.claude/skills/browser-use && python server.py start &
```

## Direct Mode (No API Key Needed)

Claude controls browser directly via Actor API:

```bash
# Start server
python ~/.claude/skills/browser-use/server.py start &

# Navigate
python server.py call '{"tool": "navigate", "args": {"url": "https://example.com"}}'

# Get page state + screenshot
python server.py call '{"tool": "get_state", "args": {"include_screenshot": true}}'

# Click element
python server.py call '{"tool": "click", "args": {"index": 0}}'

# Type text
python server.py call '{"tool": "type", "args": {"index": 0, "text": "search query"}}'

# Press key
python server.py call '{"tool": "press_key", "args": {"key": "Enter"}}'
```

## Tool Reference

### Page Tools
| Tool | Description |
|------|-------------|
| `navigate` | Go to URL |
| `go_back` / `go_forward` | Browser history navigation |
| `reload` | Refresh page |
| `get_state` | Get DOM + optional screenshot |
| `screenshot` | Capture current view |
| `evaluate` | Run JavaScript |
| `press_key` | Keyboard input |

### Element Tools
| Tool | Description |
|------|-------------|
| `find_elements` | Find by selector/text |
| `click` | Click element by index |
| `type` | Input text into element |
| `hover` | Mouse over element |
| `check` | Toggle checkbox |
| `select_option` | Dropdown selection |
| `drag_to` | Drag element |

### Tab Management
| Tool | Description |
|------|-------------|
| `list_tabs` | Show open tabs |
| `switch_tab` | Focus a tab |
| `close_tab` | Close a tab |

## Workflow Pattern

```
1. navigate → go to target URL
2. get_state → understand page structure
3. find_elements → locate target elements
4. click / type → interact
5. get_state → verify result
6. screenshot → capture evidence
```

## Requirements
- Python 3.8+
- `pip install browser-use`
- `playwright install chromium`

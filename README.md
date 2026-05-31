# 🌸 Marathi Mitra — MCP Server

MCP server that connects Claude Desktop to a fine-tuned Phi-3 Mini model
for Marathi vocabulary learning.

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-SDK-orange)](https://github.com/modelcontextprotocol/python-sdk)
[![Model](https://img.shields.io/badge/🤗-Model-yellow)](https://huggingface.co/ninadp/marathi-mitra-phi3-v2)

---

## What It Does

Exposes Marathi vocabulary learning tools to Claude Desktop via the
Model Context Protocol (MCP). Your fine-tuned model runs on HF Spaces
and is called via the Gradio API.

```
You:    "Teach me butterfly in Marathi"
Claude: calls teach_word("butterfly")
        → calls HF Spaces API
        → fine-tuned Phi-3 Mini generates lesson
        → Claude presents result naturally

"🌸 Butterfly in Marathi is फुलपाखरू (Phul-pakh-roo)!
 📖 फुलपाखरू फुलांवर बसते.
 Want to learn another word?"
```

---

## Architecture

```
Claude Desktop
     ↕ stdin/stdout (local pipe)
  server.py  ← this repo
     ↕ HTTP (internet)
  HF Spaces Gradio App
     ↕
  Fine-tuned Phi-3 Mini v2
```

Two connections:
- **Local** — Claude Desktop ↔ server.py via stdio (no internet)
- **Internet** — server.py ↔ HF Spaces via HTTP (gradio_client)

---

## Tools Available

| Tool | Description | Args |
|------|-------------|------|
| `teach_word` | Full Marathi lesson for any English word | `word: str` |
| `word_of_the_day` | Random daily vocabulary word | none |
| `quiz_me` | Quiz yourself on a word | `word: str` |
| `get_vocabulary_list` | Browse words by category | `category: str` |

### Example Conversations

```
"Teach me sun in Marathi"
"What's today's Marathi word?"
"Quiz me on butterfly"
"Show me all animal words"
"Teach me 5 nature words"
"Make flashcards for family words"
```

---

## Tech Stack

| Component | Tool |
|-----------|------|
| MCP Framework | Anthropic MCP SDK (FastMCP) |
| HF Spaces Client | gradio-client |
| Model | Fine-tuned Phi-3 Mini v2 (QLoRA) |
| Transport | stdio (stdin/stdout) |
| Protocol | JSON-RPC 2.0 (MCP) |

---

## Setup

### 1. Clone repo

```bash
git clone https://github.com/ninadparab/marathi-mitra-mcp.git
cd marathi-mitra-mcp
```

### 2. Install dependencies

```bash
# Python 3.11+ recommended
pip install mcp gradio-client
```

### 3. Find Claude Desktop config location

```
Windows: %APPDATA%\Local\Packages\Claude_*\LocalCache\Roaming\Claude\
Mac:     ~/Library/Application Support/Claude/
```

**Easiest way:** Open Claude Desktop → Settings → Developer → Edit Config

### 4. Add to config

```json
{
  "mcpServers": {
    "marathi-mitra": {
      "command": "C:\\Users\\YOUR_USERNAME\\marathi-mitra-mcp\\start_server.bat",
      "args": []
    }
  }
}
```

### 5. Create start_server.bat (Windows)

```bat
@echo off
"C:\path\to\python.exe" "C:\path\to\marathi-mitra-mcp\server.py"
```

Find your Python path:
```bash
py -3.11 -c "import sys; print(sys.executable)"
```

### 6. Restart Claude Desktop completely

```
Task Manager → End Task on Claude.exe
Then reopen Claude Desktop
Settings → Developer → marathi-mitra should show "connected"
```

---

## Note on Response Time

The model runs on CPU on HF Spaces free tier.
Each response takes **2-5 minutes**.

For faster responses:
- Upgrade HF Spaces to T4 GPU ($0.60/hr) → ~10 seconds
- Pause GPU when not using

---

## Related Repos

| Repo | Description |
|------|-------------|
| [marathi-mitra](https://github.com/ninadparab/marathi-mitra) | Training code, notebooks, dataset |
| [marathi-mitra-phi3-v2](https://huggingface.co/ninadp/marathi-mitra-phi3-v2) | Fine-tuned model on HF Hub |
| [marathi-mitra (Spaces)](https://huggingface.co/spaces/ninadp/marathi-mitra) | Live Gradio app |

---

## License

MIT

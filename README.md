# 🌸 Marathi Mitra — MCP Server

MCP server that exposes Marathi vocabulary learning tools to Claude Desktop.
Powered by a fine-tuned Phi-3 Mini model hosted on Hugging Face.

## What It Does

Connects your fine-tuned Marathi model to Claude Desktop so you can learn
Marathi through natural conversation with Claude.

```
You:   "Teach me butterfly in Marathi"
Claude: calls teach_word("butterfly")
        "फुलपाखरू (Phul-pakh-roo)! 🦋
         The butterfly sits on flowers...
         Want to learn another word?"
```

## Tools Available

| Tool | Description |
|------|-------------|
| `teach_word(word)` | Full Marathi lesson for any English word |
| `word_of_the_day()` | Random daily vocabulary word |
| `quiz_me(word)` | Quiz yourself on a word |
| `get_vocabulary_list(category)` | Browse available words |

## Setup

### 1. Install dependencies

```bash
pip install mcp gradio-client requests
```

### 2. Find your Claude Desktop config file

```
Mac:     ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
```

### 3. Add MCP server to config

```json
{
  "mcpServers": {
    "marathi-mitra": {
      "command": "python",
      "args": ["/FULL/PATH/TO/marathi-mitra-mcp/server.py"]
    }
  }
}
```

Replace `/FULL/PATH/TO/` with your actual path.

**Mac example:**
```json
{
  "mcpServers": {
    "marathi-mitra": {
      "command": "python",
      "args": ["/Users/yourname/marathi-mitra-mcp/server.py"]
    }
  }
}
```

**Windows example:**
```json
{
  "mcpServers": {
    "marathi-mitra": {
      "command": "python",
      "args": ["C:\\Users\\yourname\\marathi-mitra-mcp\\server.py"]
    }
  }
}
```

### 4. Restart Claude Desktop

Quit completely and reopen.
You should see a 🔨 hammer icon in Claude Desktop
indicating tools are available.

## Example Conversations

```
"Teach me the Marathi word for sun"
"What's today's Marathi word?"
"Quiz me on butterfly"
"Show me all animal words"
"Teach me 5 nature words"
"Make flashcards for family words"
```

## Architecture

```
Claude Desktop
    ↓ MCP protocol
server.py (this repo)
    ↓ Gradio client
HF Spaces (ninadp/marathi-mitra)
    ↓ model inference
Fine-tuned Phi-3 Mini v2
```

## Related

- [Marathi Mitra App](https://huggingface.co/spaces/ninadp/marathi-mitra)
- [Model on HF Hub](https://huggingface.co/ninadp/marathi-mitra-phi3-v2)
- [Training Code](https://github.com/ninadparab/marathi-mitra)

## License

MIT

# 🧪 Lab 08 – MCP Server: Web Search with Perplexity

## 🎯 Lab Objective

In this lab, you will build an **MCP Server capable of performing live web searches** using the **Perplexity API**.

By the end of this lab, an MCP client (Claude Desktop or MCP Inspector) will be able to:

* Submit natural language queries
* Trigger live web searches
* Receive up-to-date information from the internet
* Use real-time search results as reasoning context

This lab introduces **web-connected intelligence** via MCP.

---

## 🧠 What You Will Learn

* How to integrate **external LLM APIs** into an MCP Server
* How to securely manage API keys using `.env`
* How to expose **live web search** as an MCP tool
* How runtime configuration impacts dependency resolution in Claude

---

## ⚠️ Prerequisites & Requirements

### Required Accounts

* **Perplexity account**
* **Perplexity API key**
* Available API credits

Create your Perplexity account and API key **before starting this lab**.

---

## 🔐 API Key Configuration

Create a file named **`.env`** in the same directory as `websearch.py`:

```env
PERPLEXITY_API_KEY="YOUR_API_KEY_HERE"
```

### ⚠️ Security Best Practices

* Do **not** commit `.env` to GitHub
* Add `.env` to `.gitignore`
* Treat the key as a secret

---

## 📌 Prerequisites

* Python installed
* UV installed
* Internet access
* Claude Desktop installed
* MCP CLI available

---

## 🧱 Step 1 – Initialize the Project

Open a terminal in your project directory and run:

```bash
uv init
```

* Initializes a new Python project
* Uses the **current directory name** as the project name by default

Optional:

```bash
uv init my-project-name
```

---

## 🧪 Step 2 – Create a Virtual Environment

```bash
uv venv
```

* Creates a `.venv` directory
* Isolates dependencies for this MCP Server

---

## ▶️ Step 3 – Activate the Virtual Environment (Windows)

```bash
.\.venv\Scripts\activate
```

* Terminal prompt changes
* Confirms the virtual environment is active

---

## 📦 Step 4 – Install Required Packages

```bash
uv add mcp[cli]
uv add openai
uv add python-dotenv
```

### Why these packages?

* **mcp[cli]** → MCP server, client, inspector, installer
* **openai** → OpenAI-compatible SDK used by Perplexity
* **python-dotenv** → Secure environment variable loading

---

## 🧑‍💻 Step 5 – Create the MCP Server (`websearch.py`)

Create `websearch.py` with the following content:

```python
from __future__ import annotations

import os

from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "PERPLEXITY_API_KEY not found in .env file. "
        "Create a .env file and add: PERPLEXITY_API_KEY=..."
    )

mcp = FastMCP("Web Search")

@mcp.tool()
def perform_websearch(query: str) -> str:
    """
    Performs a web search using Perplexity.
    Args:
        query: the query to search on the web.
    """
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that searches the web and responds to questions.",
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.perplexity.ai",
    )

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )

    return response.choices[0].message.content


def main():
    # Force stdio transport (recommended)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
```

---

## 🧠 How This MCP Server Works

* Exposes one tool: **`perform_websearch`**
* Uses Perplexity via an OpenAI-compatible API
* Sends the query as a chat completion
* Returns **live web-informed responses**

This is **real-time information**, not static model knowledge.

---

## 🔍 Step 6 – Test with MCP Inspector

Before installing into Claude, validate the server locally.

```bash
mcp dev websearch.py
```

### In the MCP Inspector UI

1. Click **Connect**
2. Go to **Tools**
3. Click **List Tools**
4. Select **perform_websearch**
5. Example query:

```
Search the web and tell me the most important global news today.
```

6. Click **Run Tool**
7. Wait for the response

---

## 🔌 Step 7 – Install the MCP Server in Claude Desktop

### Option A – Automatic Installation

```bash
mcp install websearch.py
```

⚠️ **Important:**
In practice, this method caused runtime issues related to **dependency resolution and environment activation**.

---

## ⚠️ Important Note – Claude Runtime & Virtual Environment

During testing, Claude failed to execute the MCP Server correctly because it was **not running inside the UV-managed environment**, causing dependency and SDK resolution issues.

### 🧠 Why This Happens

* `mcp install` may register the server using **system Python**
* Dependencies installed via `uv` live in a separate environment
* Claude does not automatically activate `.venv`
* Result: runtime errors or missing libraries

---

## ✅ Solution – Explicit UV Execution in Claude Configuration

Manually update Claude’s MCP configuration to ensure the server is executed with **`uv run`**.

### 📄 Update `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "Web Search": {
      "command": "C:\\Users\\Raphael\\AppData\\Roaming\\Python\\Python312\\Scripts\\uv.EXE",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 08 - MCP Server for Web Search with Perplexity",
        "run",
        "websearch.py"
      ]
    }
  }
}
```

> 🔧 Adjust paths according to your local environment.

---

## 🔄 Step 8 – Restart Claude Desktop

After editing the config:

* Fully **Quit** Claude Desktop (use *Quit*, not just close)
* Reopen Claude to load the new configuration

---

## 🧪 Step 9 – Test in Claude Desktop

Try prompts such as:

> **“Search the web and tell me the most important news in the world today.”**

or

> **“Do a web search and summarize the latest AI developments.”**

### ✅ Expected Behavior

* Claude requests permission to call **Web Search**
* The MCP Server runs via `uv`
* Perplexity API is called successfully
* Claude returns **live web-based information**
* Tool appears in Claude’s connectors/tools panel

---

## ⚠️ Cost & Security Considerations

* Each query consumes **Perplexity credits**
* Avoid uncontrolled loops or frequent polling
* Recommended improvements:

  * Rate limiting
  * Caching
  * Query validation
  * Audit logging

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* A working MCP Server for live web search
* Secure API key handling
* Correct runtime configuration in Claude
* Real-time web intelligence integrated with an LLM

---

## 📌 Key Takeaways

* MCP Servers often require **explicit runtime control**
* Environment isolation matters when integrating with Claude
* Web search dramatically expands LLM usefulness
* This pattern enables:

  * Research assistants
  * News monitoring agents
  * Threat intelligence tools
  * Market analysis copilots

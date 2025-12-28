# 🧪 Lab 14 – Memory Tracker with OpenAI Vectors (RAG)

## 🎯 Lab Objective

In this lab, you will build an **MCP Server that acts as a memory layer** for interactions with MCP Hosts (such as Claude Desktop).

The goal is to allow the LLM to:

* **Store conversations or important information**
* **Retrieve past memories later**
* Use **vector embeddings (RAG)** to enable semantic search over stored memories

All vectors will be:

* Generated using **OpenAI Embeddings**
* Stored and queried via the **OpenAI platform**

---

## 🧠 Use Case Example

Imagine you are planning a trip:

1. You ask Claude to research destinations
2. You explicitly ask Claude to **save this information**
3. The MCP Server stores the interaction as vectors
4. Days later, you ask:

   > “What did we decide about the trip?”
5. The MCP Server retrieves the relevant memory using semantic search

This lab implements exactly this behavior.

---

## 🧩 Architecture Overview

```
Claude Desktop
      │
      │  (Tool call)
      ▼
MCP Memory Server
      │
      │  (Embeddings API)
      ▼
OpenAI Vector Storage
```

* Claude does **not** store memory by itself
* Memory persistence is delegated to the MCP Server
* Retrieval uses **semantic similarity**, not keywords

---

## ⚠️ Prerequisites & Requirements

### Required Accounts

* **OpenAI Account**
* **OpenAI API Key**
* **Available API credits**

👉 Create your OpenAI account and API key **before starting this lab**.

---

## 🔐 API Key Configuration

Create a file named **`.env`** in the same directory as `server.py`:

```env
OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

### ⚠️ Security Best Practices

* ❌ Do NOT commit `.env` to GitHub
* ✅ Add `.env` to `.gitignore`
* 🔐 Treat the API key as a secret

---

## 📌 General Prerequisites

* Python installed (3.12+ recommended)
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

This initializes a new Python project.

To explicitly set a project name:

```bash
uv init my-project-name
```

---

## 🧪 Step 2 – Create a Virtual Environment

```bash
uv venv
```

This creates a `.venv` directory at the project root, isolating dependencies.

---

## ▶️ Step 3 – Activate the Virtual Environment (Windows)

```bash
.\.venv\Scripts\activate
```

The terminal prompt will change, confirming that the virtual environment is active.

---

## 📦 Step 4 – Install Required Packages

```bash
uv add mcp[cli] openai
```

This installs:

* MCP core libraries
* MCP CLI
* OpenAI SDK

---

## 🧠 Step 5 – MCP Memory Server

At this point, the MCP Server is already implemented in:

```
server.py
```

This server exposes tools that allow:

* Saving memories (vectorized using OpenAI embeddings)
* Searching stored memories using semantic similarity

---

## 🧪 Step 6 – Test Using MCP Inspector

Run the MCP Inspector:

```bash
mcp dev server.py
```

### In the MCP Inspector UI:

1. Open the browser
2. Click **Connect**
3. Go to **Tools**
4. Click **List Tools**
5. Use the tool **`save_memory`**

   * Write any text
   * Click **Run Tool**
6. Then use **`search_memory`**

   * Enter a related query
   * Verify that the stored memory is retrieved

✅ This confirms that:

* Embeddings are being generated
* Vectors are stored
* Semantic search is working

---

## 🤖 Step 7 – Integrate with Claude Desktop

### Configure Claude MCP Server

Edit `claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "Memory": {
      "command": "C:\\Users\\Raphael\\AppData\\Roaming\\Python\\Python312\\Scripts\\uv.EXE",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 14 - Lab 14 - Memory Tracker with OpenAI Vectors RAG",
        "run",
        "server.py"
      ]
    }
  }
}
```

> ⚠️ Adjust the directory path to match your local environment.

---

## 🔄 Step 8 – Restart Claude Desktop

* Fully **quit Claude Desktop** (use Quit, not just close)
* Reopen Claude so the new MCP Server is loaded

---

## 🧪 Step 9 – Test in Claude Desktop

### Example Flow

1. Ask Claude to perform any research:

   > “Do some research about best places to visit in Italy”

2. Then ask:

   > “Store this result in memory”

3. Later, ask:

   > “What did we discuss about traveling to Italy?”

Claude will:

* Call the MCP Memory Server
* Perform a semantic search
* Retrieve the stored context

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* An MCP Server acting as a **memory store**
* Semantic search powered by **OpenAI embeddings**
* A working **RAG-based memory system**
* Claude Desktop enhanced with **long-term memory capabilities**

---

## 📌 Key Takeaways

* MCP enables **externalized memory**
* Memory is explicit, not automatic
* Vector search enables semantic recall
* OpenAI embeddings power RAG workflows
* This pattern scales to:

  * Knowledge bases
  * User profiles
  * Project context
  * Long-running agents

# 🧪 Lab 05 – MCP Server: Local Files

## 🎯 Lab Objective

In this lab, you will build an **MCP Server that allows an LLM to read from and write to a local file** (`notes.txt`).

This enables use cases such as:

* “Summarize text X and save the notes locally”
* “Read my saved notes”
* Persistent local memory for LLM-assisted workflows

By the end of this lab, Claude will be able to **store and retrieve information from your local filesystem via MCP**.

---

## ⚠️ Security Note

This lab demonstrates **local file access**, which is powerful and potentially sensitive.

Key points:

* The MCP Server runs **locally**
* File access is **explicitly granted via tools**
* Claude must ask for **permission** before invoking these tools

This lab intentionally keeps the scope minimal (`notes.txt`) to illustrate **safe, controlled local persistence**.

---

## 📌 Prerequisites

* Python installed
* UV installed
* VS Code (recommended)
* Claude Desktop installed
* MCP CLI available

---

## 🧱 Step 1 – Initialize the Project

Open a terminal in your project directory and run:

```bash
uv init
```

* Initializes a new Python project
* The project name defaults to the **current directory name**

To explicitly set a name:

```bash
uv init my-project-name
```

---

## 🧪 Step 2 – Create a Virtual Environment

```bash
uv venv
```

* Creates a `.venv` directory at the project root
* Isolates dependencies for this project

---

## ▶️ Step 3 – Activate the Virtual Environment (Windows)

```bash
.\.venv\Scripts\activate
```

* The terminal prompt will change
* This confirms the virtual environment is active

---

## 📦 Step 4 – Install the MCP Package

```bash
uv add mcp[cli]
```

This installs:

* MCP core libraries
* MCP CLI utilities
* Client and server helpers

---

## 🧑‍💻 Step 5 – Create the MCP Server (`local.py`)

Create a file named `local.py` with the following content:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("LocalNotes")

@mcp.tool()
def add_note_to_file(content: str) -> str:
    """
    Appends the given content to the user's local notes.
    Args:
        content: The text content to append.
    """

    filename = 'notes.txt'

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Content appended to {filename}."
    except Exception as e:
        return f"Error appending to file {filename}: {e}"


@mcp.tool()
def read_notes() -> str:
    """
    Reads and returns the contents of the user's local notes.
    """

    filename = 'notes.txt'

    try:
        with open(filename, "r", encoding="utf-8") as f:
            notes = f.read()
        return notes if notes else "No notes found."
    except FileNotFoundError:
        return "No notes file found."
    except Exception as e:
        return f"Error reading file {filename}: {e}"

mcp.run()
```

---

## 🧠 What This MCP Server Does

* Creates an MCP Server named **LocalNotes**
* Exposes two tools:

  * `add_note_to_file` → appends text to `notes.txt`
  * `read_notes` → reads and returns file contents
* Uses plain local file I/O
* Keeps scope limited to a single file

---

## 📄 Step 6 – Create the Local Notes File

Create a file named:

```text
notes.txt
```

* This file will be used by the MCP Server
* The LLM will read from and write to this file via MCP tools

---

## 🔍 Step 7 – Test with MCP Inspector

Before integrating with Claude, validate the server locally.

### ▶️ Start MCP Inspector

```bash
mcp dev local.py
```

* MCP Inspector will start
* A browser window will open

---

### 🌐 Using the MCP Inspector Web UI

1. Click **Connect**
2. Go to the **Tools** tab
3. Click **List Tools**
4. You should see:

   * `add_note_to_file`
   * `read_notes`

#### ✏️ Test Writing

* Open `add_note_to_file`
* Enter some text
* Click **Run Tool**

#### 📖 Test Reading

* Open `read_notes`
* Click **Run Tool**
* Verify the previously added text is returned

Also confirm that the content exists in `notes.txt`.

---

## 🔌 Step 8 – Install the MCP Server in Claude

Install the MCP Server so Claude can use it:

```bash
mcp install local.py
```

This command:

* Registers the MCP Server automatically
* Updates `claude_desktop_config.json`
* Makes the tools available to Claude Desktop

---

## 🔄 Step 9 – Restart Claude Desktop

* Fully quit Claude Desktop (use **Quit**, not just close)
* Reopen the application

---

## 🧪 Step 10 – Test in Claude Desktop

In Claude, run the following prompts:

### ✏️ Write Notes

> **“Tell me 10 top-rated LLM models and save this information in my local notes.”**

Expected behavior:

* Claude asks permission to call **LocalNotes**
* `add_note_to_file` is invoked
* Content is written to `notes.txt`

---

### 📖 Read Notes

> **“Read my local notes and tell me what is written there.”**

Expected behavior:

* Claude calls `read_notes`
* The contents of `notes.txt` are returned and summarized

---

## ✅ Expected Outcome

By the end of this lab:

* You created an MCP Server with local file access
* Validated it using MCP Inspector
* Installed it into Claude Desktop
* Enabled Claude to persist and retrieve local information

---

## 📌 Key Takeaways

* MCP enables **explicit, permission-based local persistence**
* File I/O is exposed safely through tools
* LLMs can act as:

  * Note takers
  * Memory assistants
  * Workflow augmenters
* This pattern is foundational for:

  * Personal knowledge bases
  * Local agent memory
  * Secure on-device AI workflows

---

## 📌 Conclusion

This lab demonstrates one of MCP’s most powerful features:
**bridging LLM reasoning with local state**, safely and transparently.

You now have:

* Local memory
* Controlled access
* Repeatable persistence via MCP

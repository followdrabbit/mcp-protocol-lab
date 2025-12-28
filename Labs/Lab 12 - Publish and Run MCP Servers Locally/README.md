# 🧪 Lab 12 – Publish and Run MCP Servers Locally

## 🎯 Lab Objective

In this lab, you will learn **how to package, publish, install, and run an MCP Server locally** using a **GitHub-hosted Python package**, following the **same execution model used by community MCP servers** (such as the Airbnb MCP).

⚠️ **Important Scope Clarification**

Although MCP Servers *can* be executed remotely (VMs, containers, web services), **this lab does NOT cover remote execution**.

👉 **This lab focuses exclusively on:**

* Packaging an MCP Server
* Hosting the source code on GitHub
* Installing the package on the client machine
* Executing the MCP Server **locally** via `uvx`
* Connecting Claude Desktop to that local execution

---

## 🧠 How Local MCP Distribution Works

In the MCP ecosystem, **local execution via packages** is a first-class and widely adopted model.

### Example: Airbnb MCP Server

When Claude Desktop is configured like this:

```json
{
  "mcpServers": {
    "airbnb": {
      "command": "npx",
      "args": [
        "-y",
        "@openbnb/mcp-server-airbnb",
        "--ignore-robots-txt"
      ]
    }
  }
}
```

Claude is effectively running:

```bash
npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt
```

### What Actually Happens

1. The package is downloaded from **NPM**
2. The MCP Server code is installed locally
3. The server is executed **on the user’s machine**
4. Claude communicates with it via stdio

📦 Airbnb MCP package source:
[https://www.npmjs.com/package/@openbnb/mcp-server-airbnb](https://www.npmjs.com/package/@openbnb/mcp-server-airbnb)

---

## 🧠 Python Equivalent of `npx`

In Python, the equivalent of `npx` is **`uvx`**.

This lab demonstrates how to:

* Publish an MCP Server to GitHub
* Install it dynamically via `uvx`
* Run it locally on-demand
* Integrate it with Claude Desktop

---

## 📌 Prerequisites

* Python 3.12+
* UV installed
* GitHub account
* MCP CLI available
* Claude Desktop

---

## 🧱 Step 1 – Initialize the Project

```bash
uv init
```

Optional custom name:

```bash
uv init my-project-name
```

---

## 🧪 Step 2 – Create a Virtual Environment

```bash
uv venv
```

---

## ▶️ Step 3 – Activate the Virtual Environment (Windows)

```bash
.\.venv\Scripts\activate
```

---

## 📦 Step 4 – Install MCP

```bash
uv add mcp[cli]
```

---

## 🧑‍💻 Step 5 – Create the Package Structure

Create the following structure:

```
src/
└── mcpserver/
    ├── __init__.py
    ├── __main__.py
    └── deployment.py
```

---

### `__init__.py`

Leave empty.

---

### `__main__.py`

```python
from mcpserver.deployment import mcp

def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

This defines the **executable entry point** of the package.

---

### `deployment.py`

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

This is the **actual MCP Server logic**.

---

## ⚙️ Step 6 – Configure `pyproject.toml`

Add the following configuration:

```toml
[project.scripts]
mcp-server = "mcpserver.__main__:main"

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

### Example Final `pyproject.toml`

```toml
[project]
name = "lab-12-local-mcp-server"
version = "0.1.0"
description = "Demo MCP Server packaged for local execution"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "mcp[cli]>=1.25.0",
]

[project.scripts]
mcp-server = "mcpserver.__main__:main"

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

---

## 🌍 Step 7 – Publish the Package to GitHub

1. Create a **public GitHub repository**
2. Do **not** initialize it
3. Push your local project

📦 Example repository used in this lab:
[https://github.com/followdrabbit/mcp-server-lab12](https://github.com/followdrabbit/mcp-server-lab12)

---

## 📥 Step 8 – Install and Run Locally Using `uvx`

```bash
uvx --from "git+https://github.com/followdrabbit/mcp-server-lab12.git" mcp-server
```

### What This Command Does

* Downloads the repository from GitHub
* Builds the Python package
* Installs dependencies
* Executes the MCP Server **locally**

➡️ **This is the Python equivalent of `npx`**

---

## 🔌 Step 9 – Integrate with Claude Desktop (Local Execution)

Update `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "Add two numbers": {
      "command": "C:\\Users\\Raphael\\AppData\\Roaming\\Python\\Python312\\Scripts\\uvx.EXE",
      "args": [
        "--from",
        "git+https://github.com/followdrabbit/mcp-server-lab12.git",
        "mcp-server"
      ]
    }
  }
}
```

➡️ Claude will:

* Download the package
* Run the MCP Server locally
* Communicate via stdio

---

## 🔄 Step 10 – Restart Claude Desktop

* Fully **Quit** Claude Desktop
* Reopen to load the MCP Server

---

## 🧪 Step 11 – Test in Claude

Prompt:

> **“Add these two numbers: 10 and 43”**

### ✅ Expected Result

```
53
```

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* A packaged MCP Server
* Hosted on GitHub
* Installed dynamically on the client
* Executed locally
* Integrated with Claude Desktop

---

## 📌 Key Takeaways

* MCP Servers are often **executed locally**, not remotely
* Distribution ≠ hosting a live service
* `uvx` plays the same role as `npx`
* This model enables:

  * Open-source MCP servers
  * Easy sharing
  * Safe local execution
  * Reproducibility

# 🧪 Lab 11 – MCP Server for Resources

## 🎯 Lab Objective

In this lab, you will build an **MCP Server that exposes Resources** instead of tools or prompts.

MCP **Resources** allow LLMs to:

* Discover structured information via URIs
* Navigate hierarchical or relational data
* Retrieve data **without executing actions**
* Treat data as *addressable knowledge*, not commands

By the end of this lab, Claude will be able to:

* List available resources
* Resolve resource URIs
* Fetch inventory data using resource paths

---

## 🧠 What Are MCP Resources?

Unlike **tools** (actions) and **prompts** (templates), **resources**:

* Represent **read-only data**
* Are identified by **URIs**
* Can include **path parameters**
* Behave like a structured knowledge graph

Think of MCP Resources as:

* A virtual filesystem
* An API without verbs
* A semantic data catalog

Example URIs:

* `inventory://overview`
* `inventory://Coffee/id`
* `inventory://123/price`

---

## 📌 Prerequisites

* Python installed
* UV installed
* MCP CLI available
* Claude Desktop (for integration testing)

---

## 🧱 Step 1 – Initialize the Project

Open a terminal in your project directory:

```bash
uv init
```

* Initializes a new Python project
* Project name defaults to the **current directory name**

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
* Confirms the environment is active

---

## 📦 Step 4 – Install Required Packages

```bash
uv add mcp[cli]
```

> ℹ️ No additional libraries are required for Resources.

---

## 🧑‍💻 Step 5 – Create the MCP Server (`resources.py`)

Create a file named `resources.py` with the following content:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Resources")

@mcp.resource("inventory://overview")
def get_inventory_overview() -> str:
    """
    Returns an overview of the inventory.
    """
    overview = """
Inventory Overview:
- Coffee
- Tea
- Cookies
"""
    return overview.strip()


inventory_id_to_price = {
    "123": "6.99",
    "456": "17.99",
    "789": "84.99"
}

inventory_name_to_id = {
    "Coffee": "123",
    "Tea": "456",
    "Cookies": "789"
}


@mcp.resource("inventory://{inventory_id}/price")
def get_inventory_price_from_inventory_id(inventory_id: str) -> str:
    """
    Returns the price of an item given its inventory ID.
    """
    return inventory_id_to_price[inventory_id]


@mcp.resource("inventory://{inventory_name}/id")
def get_inventory_id_from_inventory_name(inventory_name: str) -> str:
    """
    Returns the inventory ID given the item name.
    """
    return inventory_name_to_id[inventory_name]


if __name__ == "__main__":
    mcp.run()
```

---

## 🧠 How This MCP Server Works

* Defines **three resources**:

  * `inventory://overview`
  * `inventory://{inventory_name}/id`
  * `inventory://{inventory_id}/price`
* Resources can reference each other logically
* Claude (or Inspector) can navigate data step-by-step

Example resolution flow:

1. Get overview
2. Choose item name
3. Resolve item ID
4. Resolve price

---

## 🔍 Step 6 – Test with MCP Inspector

Run the MCP Inspector:

```bash
mcp dev resources.py
```

### In the MCP Inspector UI

1. Click **Connect**
2. Go to **Resources**
3. Click **List Resources**
4. Test the following URIs:

* `inventory://overview`
* `inventory://Coffee/id`
* `inventory://123/price`

### ✅ Expected Results

* Inventory overview text
* Item ID returned for a name
* Price returned for an ID

---

## 🔌 Step 7 – Install the MCP Server in Claude Desktop

```bash
mcp install resources.py
```

---

## ⚠️ Important Note – Claude Runtime Configuration

As seen in previous labs, Claude may fail to execute MCP Servers correctly if it does not use the **UV-managed environment**.

### ✅ Correct `claude_desktop_config.json` Entry

```json
{
  "mcpServers": {
    "Resources": {
      "command": "C:\\Users\\Raphael\\AppData\\Roaming\\Python\\Python312\\Scripts\\uv.EXE",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 11 - MCP Server for Resources",
        "run",
        "resources.py"
      ]
    }
  }
}
```

> 🔧 Adjust paths according to your local environment.

---

## 🔄 Step 8 – Restart Claude Desktop

* Fully **Quit** Claude Desktop (not just close)
* Reopen Claude so the new MCP Server is loaded

---

## 🧪 Step 9 – Test in Claude Desktop

### Method – Resource Picker

1. Click the **“+”** icon in Claude
2. Select **Add from server**
3. Choose **Resources**
4. Select **get_inventory_overview**

Claude will fetch and display the inventory data.

You can then ask follow-up questions like:

* “What is the price of Coffee?”
* “Show me the ID of Cookies”

Claude will resolve the resources automatically.

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* An MCP Server exposing structured Resources
* URI-based data navigation
* Successful integration with Claude Desktop
* A clear separation between:

  * **Data (resources)**
  * **Actions (tools)**
  * **Templates (prompts)**

---

## 📌 Key Takeaways

* Resources are **read-only knowledge endpoints**
* They model relationships naturally
* Ideal for catalogs, inventories, configs, and metadata
* LLMs can traverse resources safely and deterministically

---

## 📌 Conclusion

This lab completes the **third MCP primitive**:

> **Resources transform MCP servers into structured knowledge providers.**
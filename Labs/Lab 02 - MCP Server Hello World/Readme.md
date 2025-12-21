# 🧪 Lab 02 – Creating a Hello World MCP Server

## 🎯 Lab Objective

In this lab, you will **create your first MCP Server from scratch**, implement a simple tool, test it locally using the **MCP Inspector**, and then integrate it with **Claude Desktop**.

By the end of this lab, Claude will be able to call your custom MCP Server and execute a tool you created.

---

## ⚠️ Important Note (Before You Start)

Create this project in a directory that is **NOT synchronized** with cloud storage tools such as:

* Google Drive
* OneDrive
* Dropbox

These tools often interfere with Python virtual environments and package resolution, causing unexpected runtime errors.

---

## 🧰 Tooling Choice

This lab uses **UV**, the package and environment manager recommended by the MCP ecosystem.

> 💡 You may use `pip` instead if you prefer, but all examples in this lab use **UV**.

---

## 📌 Prerequisites

* VS Code
* Python installed
* Node.js (for MCP tooling)
* UV installed
* Claude Desktop installed

---

## 🛠️ Step 1 – Open the Terminal in VS Code

Open your project directory in **VS Code**, then open the integrated terminal.

---

## 🧱 Step 2 – Initialize the Project

```bash
uv init
```

* This command initializes a new Python project
* The project name will default to the **current directory name**
* To use a different name, pass it explicitly:

  ```bash
  uv init my-project-name
  ```

---

## 🧪 Step 3 – Create a Virtual Environment

```bash
uv venv
```

* A `.venv` directory will be created at the project root
* This isolates dependencies for this MCP Server

---

## ▶️ Step 4 – Activate the Virtual Environment (Windows)

```bash
.\.venv\Scripts\activate
```

* The terminal prompt will change
* This confirms the virtual environment is active

---

## 📦 Step 5 – Install the MCP Package

```bash
uv add mcp[cli]
```

This installs:

* MCP core libraries
* MCP CLI tools (including Inspector and installer)

---

## 🧑‍💻 Step 6 – Create the MCP Server (`weather.py`)

Create a file named `weather.py` and add the following code:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(location: str) -> str:
    """
    Gets the weather given a location
    Args:
        location: location, can be city, country, state, etc.
    """
    return "The weather is hot and dry"

if __name__ == "__main__":
    mcp.run()
```

### 🧠 What This Code Does

* Creates an MCP Server named **Weather**
* Exposes a tool called `get_weather`
* Accepts a location string
* Returns a static response (Hello World–style behavior)

---

## 🔍 Step 7 – Test the Server with MCP Inspector

Running an MCP Server alone does nothing visible to the user.
To test it before integrating with a client, we use the **MCP Inspector**.

### ▶️ Start the Inspector

```bash
mcp dev weather.py
```

* The CLI may ask to install additional packages — approve the installation
* MCP Inspector will:

  * Create a temporary MCP Host
  * Create a temporary MCP Client
  * Open a web UI in your browser

---

### 🌐 Using the MCP Inspector Web UI

1. Click **Connect**
2. Go to the **Tools** tab
3. Click **List Tools**
4. The `get_weather` tool should appear
5. Click on `get_weather`
6. Fill in a location (e.g., `São Paulo`)
7. Click **Run Tool**

### ✅ Expected Result

* The response:

  ```
  The weather is hot and dry
  ```
* This confirms your MCP Server works correctly

---

## 🔌 Step 8 – Install the MCP Server in Claude (JSON Configuration)

### 📄 Manual Configuration

Open **Claude Desktop** and navigate to:

```
File → Settings → Developer → Edit config
```

Edit the file `claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 02 - MCP Server Hello World",
        "run",
        "weather.py"
      ]
    }
  }
}
```

> ⚠️ Make sure the directory path matches your local environment.

---

### 🧩 If You Already Have the Airbnb MCP Server Configured

Use the combined configuration:

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
    },
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 02 - MCP Server Hello World",
        "run",
        "weather.py"
      ]
    }
  }
}
```

---

### 🔄 Restart Claude Desktop

* Fully quit Claude Desktop (use **Quit**, not just close)
* Reopen the application

---

## 🧪 Step 9 – Validate in Claude Desktop

Ask Claude:

> **“What’s the weather like in São Paulo?”**

### ✅ Expected Behavior

* Claude asks for permission to call the **Weather MCP Server**
* After authorization:

  * The MCP Server is executed
  * The `get_weather` tool is called
* The response is returned from your MCP Server

You should also see the **Weather tool listed in Claude’s connectors/tools panel**.

---

## ⚙️ Step 10 – Alternative Installation (MCP Installer)

Instead of manually editing the JSON file, you can run:

```bash
mcp install weather.py
```

This command:

* Automatically installs the MCP Server
* Updates `claude_desktop_config.json`
* Registers the server in Claude Desktop

---

## ✅ Expected Outcome

By the end of this lab:

* You created a custom MCP Server
* Tested it using MCP Inspector
* Integrated it with Claude Desktop
* Validated real tool execution via MCP

---

## 📌 Conclusion

This lab introduces the **full MCP development lifecycle**:

1. Project initialization
2. Server implementation
3. Local validation
4. Client/Host integration
5. Permission-based execution

This pattern will be reused and expanded in future labs.

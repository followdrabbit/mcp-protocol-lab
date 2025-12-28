# 🧪 Lab 06 – Screenshot and Claude Analysis (MCP Server)

## 🎯 Lab Objective

In this lab, you will create an **MCP Server capable of capturing a screenshot of the user’s screen** and sending it as an image input to **Claude Desktop**, allowing Claude to **analyze and describe what is visible on the screen**.

This lab demonstrates how MCP can bridge:

* **OS-level capabilities** (screen capture)
* **Binary data (images)**
* **LLM multimodal reasoning**

---

## 🧠 Use Cases

* “Take a screenshot and describe what’s on my screen”
* Visual debugging assistance
* UI analysis and walkthroughs
* Productivity copilots with visual context

---

## ⚠️ Privacy & Safety Warning

This lab captures the **entire screen**.

Before running:

* Close sensitive applications (banking, passwords, private messages)
* Be aware that screenshots may include confidential data
* Claude will request permission before calling the tool (depending on settings)

This lab intentionally demonstrates **controlled, explicit screen access** via MCP tools.

---

## 📌 Prerequisites

* Windows (steps assume Windows paths)
* Python installed
* UV installed
* Claude Desktop installed
* Permissions to capture the screen at OS level

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
* Isolates dependencies for this MCP Server

---

## ▶️ Step 3 – Activate the Virtual Environment (Windows)

```bash
.\.venv\Scripts\activate
```

* The terminal prompt will change
* Confirms the virtual environment is active

---

## 📦 Step 4 – Install Required Packages

Install MCP and screenshot-related dependencies:

```bash
uv add mcp[cli]
uv add pyautogui
uv add pillow
```

### Why these packages?

* **mcp[cli]** → MCP server, client, inspector, installer
* **pyautogui** → Screen capture
* **pillow** → Image processing and compression

---

## 🧑‍💻 Step 5 – Create the MCP Server (`screenshot.py`)

Create a file named `screenshot.py` with the following content:

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image

import pyautogui
import io

# Create server
mcp = FastMCP("Screenshot Demo")

@mcp.tool()
def capture_screenshot() -> Image:
    """
    Capture the current screen and return the image.
    Use this tool whenever the user requests a screenshot of their activity.
    """

    buffer = io.BytesIO()

    # If the image exceeds ~1MB, it may be rejected by Claude
    screenshot = pyautogui.screenshot()
    screenshot.convert("RGB").save(
        buffer,
        format="JPEG",
        quality=60,
        optimize=True
    )

    return Image(data=buffer.getvalue(), format="jpeg")

if __name__ == "__main__":
    mcp.run()
```

---

## 🧠 How This MCP Server Works

* `capture_screenshot()`:

  * Captures the full screen
  * Compresses the image to JPEG
  * Returns it as an MCP `Image` type
* Compression is important due to **payload size limits** enforced by some MCP hosts

---

## 🔍 Step 6 – Test with MCP Inspector

Before integrating with Claude, validate the server locally.

### ▶️ Start MCP Inspector

```bash
mcp dev screenshot.py
```

### 🌐 In the MCP Inspector Web UI

1. Click **Connect**
2. Go to **Tools**
3. Click **List Tools**
4. Click **capture_screenshot**
5. Click **Run Tool**
6. Confirm that a screenshot image is returned

✅ If the screenshot appears, the MCP Server is working correctly.

---

## 🔌 Step 7 – Install the MCP Server in Claude Desktop

### Option A – Automatic Installation

```bash
mcp install screenshot.py
```

⚠️ **Important:**
In some environments, this method may fail to load `pyautogui`.

---

## ⚠️ Important Note – Claude Installation & Virtual Environment

During testing, an error occurred because **Claude was not executing the MCP Server inside the correct virtual environment**, causing `pyautogui` to fail.

### 🧠 Why This Happens

* `mcp install` may register the server using **system Python**
* Dependencies installed via `uv` live inside `.venv`
* OS-level libraries like `pyautogui` must run from the correct environment

---

## ✅ Solution – Explicit `uv run` Configuration

Manually update Claude’s configuration file to ensure the MCP Server is executed using `uv`.

### 📄 Edit `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "Screenshot Demo": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 06 - Screenshot and Claude Analysis",
        "run",
        "screenshot.py"
      ]
    }
  }
}
```

> 🔧 Adjust the directory path to match your local environment.

---

## 🔄 Step 8 – Restart Claude Desktop

After updating the configuration:

* Fully **Quit** Claude Desktop (do not just close the window)
* Reopen the application so the new configuration is loaded

---

## 🧪 Step 9 – Test in Claude Desktop

In Claude, type:

> **“Take a screenshot and describe what is in the image.”**

### ✅ Expected Behavior

* Claude requests permission to call **Screenshot Demo**
* The MCP Server captures the screen
* The image is sent to Claude
* Claude analyzes and describes what it sees

You should also see the tool listed in Claude’s **connectors/tools panel**.

---

## 🧩 Troubleshooting

### Screenshot returns black or empty image

* Some apps block screen capture
* Remote Desktop or protected windows may interfere

### Claude rejects the image

* Reduce JPEG quality further (e.g., `quality=50`)
* Capture a smaller region (future improvement)

### Multiple monitors

* Full virtual screen may be captured
* Region-based capture can improve precision

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* A working MCP Server that captures screenshots
* Local validation via MCP Inspector
* Correct integration with Claude Desktop
* Multimodal reasoning (image → analysis) via MCP

---

## 📌 Conclusion

This lab demonstrates a **high-impact MCP pattern**:

> Connecting real-world inputs (screenshots) to LLM reasoning through explicit, permission-based tools.

It forms the foundation for:

* Visual copilots
* Debugging assistants
* UI-aware agents
* Secure multimodal automation

# 🧪 Lab 03 – MCP Client Hello World

## 🎯 Lab Objective

In this lab, you will create a **basic MCP Client** that:

* Starts an MCP Server locally
* Establishes a session using the MCP protocol
* Discovers available tools
* Calls a tool programmatically
* Receives and prints the result

This lab focuses on understanding **how an MCP Client interacts with an MCP Server at runtime**, without using a graphical host like Claude Desktop.

---

## 🧠 Conceptual Overview

In a **local execution context**:

* The **MCP Client** is responsible for:

  * Starting the MCP Server process
  * Establishing communication (stdio)
  * Initializing the MCP session
  * Listing tools and resources
  * Calling tools and handling responses

This is useful for:

* Testing
* Automation
* Embedding MCP into custom applications
* Understanding the protocol lifecycle

---

## 📌 Prerequisites

* Python installed
* UV installed
* VS Code (recommended)
* Basic understanding of async Python

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

## 🧑‍💻 Step 5 – Create the MCP Server (`weather.py`)

Although this lab focuses on the **client**, we still need a server to connect to.

Create a file called `weather.py` with the following content:

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

### 🧠 What This Server Does

* Creates an MCP Server named **Weather**
* Exposes a single tool: `get_weather`
* Accepts a `location` parameter
* Returns a static string (Hello World–style behavior)

---

## 🧑‍💻 Step 6 – Create the MCP Client (`client.py`)

Now create a file named `client.py` with the following content:

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
import traceback

server_params = StdioServerParameters(
    command="uv",
    args=["run", "weather.py"],
)

async def run():
    try:
        print("Starting stdio_client...")
        async with stdio_client(server_params) as (read, write):
            print("Client connected, creating session...")
            async with ClientSession(read, write) as session:

                print("Initializing session...")
                await session.initialize()

                print("Listing tools...")
                tools = await session.list_tools()
                print("Available tools:", tools)

                print("Calling tool...")
                result = await session.call_tool(
                    "get_weather",
                    arguments={"location": "São Paulo"}
                )

                print("Tool result:", result)

    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run())
```

---

### 🧠 How the MCP Client Works

Step by step:

1. **Defines server execution parameters**

   * Uses `uv run weather.py` to start the MCP Server

2. **Starts a stdio-based MCP connection**

   * Client and server communicate via standard input/output

3. **Creates an MCP session**

   * Initializes protocol negotiation

4. **Lists available tools**

   * Discovers tools exposed by the server

5. **Calls a tool**

   * Executes `get_weather`
   * Passes arguments programmatically
   * Receives the result

---

## ▶️ Step 7 – Run the MCP Client

Execute the client with:

```bash
uv run client.py
```

---

## ✅ Expected Output

You should see logs similar to:

```text
Starting stdio_client...
Client connected, creating session...
Initializing session...
Listing tools...
Available tools: [...]
Calling tool...
Tool result: The weather is hot and dry
```

This confirms:

* The server was started successfully
* The client connected via MCP
* Tool discovery worked
* Tool execution returned the expected result

---

## 📌 Key Takeaways

* MCP Clients can run **without a graphical host**
* The client controls:

  * Server lifecycle
  * Session initialization
  * Tool discovery
  * Tool execution
* This pattern is ideal for:

  * Automation
  * Backend services
  * Custom AI agents
  * Integration testing

---

## 📌 Conclusion

This lab completes the **MCP fundamentals triangle**:

* **Lab 01:** Existing Client ↔ Existing Server
* **Lab 02:** Creating an MCP Server
* **Lab 03:** Creating an MCP Client

You now understand MCP from **both sides of the protocol**.

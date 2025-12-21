# 🧪 Lab 04 – Configuring a Local MCP Client to Call Remote Servers

## 🎯 Lab Objective

In this lab, you will configure a **local MCP Client** to call a **remote MCP Server**, using the **Airbnb MCP Server** as a real-world example.

By the end of this lab, you will understand how:

* A local MCP Client can execute and communicate with a remote MCP Server
* Execution parameters are reused from MCP server definitions
* Tool discovery and execution work exactly the same as with local servers

---

## 🧠 Conceptual Overview

In previous labs, you learned how to:

* Integrate existing MCP clients and servers
* Build MCP servers
* Build MCP clients that start local servers

In this lab, the key difference is:

> **The MCP Client runs locally, but the MCP Server represents a remote data source and logic.**

From the client’s perspective:

* The protocol lifecycle remains the same
* Tool discovery and invocation are unchanged
* Only the **server execution command** differs

---

## 🔗 Reference MCP Server

This lab uses the **Airbnb MCP Server**, provided by the community:

👉 [https://github.com/openbnb-org/mcp-server-airbnb](https://github.com/openbnb-org/mcp-server-airbnb)

---

## 📌 Prerequisites

* Python installed
* UV installed
* Node.js / NPM installed (required to run `npx`)
* Internet access
* VS Code (recommended)

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

## 🔍 Step 5 – Analyze the Airbnb MCP Server Execution Parameters

From the Airbnb MCP Server repository, the execution parameters are defined as:

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

### 🧠 Key Insight

These parameters tell us:

* The server is executed via **npx**
* The package `@openbnb/mcp-server-airbnb` is fetched and executed on demand
* The `--ignore-robots-txt` flag is passed as a runtime argument

We will reuse these same parameters in our MCP Client.

---

## 🧑‍💻 Step 6 – Create the MCP Client (`client.py`)

Create a file named `client.py` with the following content:

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
import traceback

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
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
                    "airbnb_search",
                    arguments={"location": "Brasilia"}
                )

                print("Tool result:", result)

    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run())
```

---

## 🧠 How This MCP Client Works

1. **Defines server execution parameters**

   * Uses `npx` to run the Airbnb MCP Server
   * Downloads the package if necessary

2. **Starts a stdio-based MCP connection**

   * Client and server communicate via standard input/output

3. **Initializes the MCP session**

   * Negotiates protocol capabilities

4. **Lists available tools**

   * Discovers tools exposed by the remote server

5. **Calls a remote tool**

   * Executes `airbnb_search`
   * Passes parameters programmatically
   * Receives structured results

---

## ▶️ Step 7 – Run the MCP Client

Execute the client:

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
Tool result: {...}
```

This confirms:

* The Airbnb MCP Server was executed successfully
* Tool discovery worked
* The remote tool was invoked
* Results were returned to the local client

---

## 📌 Key Takeaways

* MCP Clients can interact with **remote servers** exactly like local ones
* Execution parameters define **where and how** the server runs
* Tool discovery and invocation remain unchanged
* This pattern enables:

  * API gateways
  * Distributed MCP architectures
  * Local agents consuming remote MCP services

---

## 📌 Conclusion

This lab demonstrates how MCP enables **location-transparent client-server interactions**.

From the client’s perspective:

* Local servers
* Remote servers
* Cloud-hosted servers

All follow the same MCP lifecycle.

This is a foundational concept for building **scalable MCP-based systems**.

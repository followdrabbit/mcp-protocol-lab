# 🧪 Lab 13 – Publish and Run MCP Servers Remotely (Streamable HTTP)

## 🎯 Lab Objective

In this lab, you will learn **how to run MCP Servers remotely** using the **Streamable HTTP transport**.

The goals of this lab are to:

* Explain how **remote MCP execution** works
* Understand **Streamable HTTP** in the MCP protocol
* Create an MCP Server that exposes itself over HTTP
* Test the server using **MCP Inspector**
* Configure **Claude Desktop** to communicate with a remote MCP Server using an adapter

---

## ⚠️ Scope Clarification (Very Important)

For simplicity and learning purposes:

* The MCP Server in this lab **runs locally**
* Communication happens via **HTTP**, exactly like a remote server
* Conceptually, this is the **same model** used when deploying to:

  * AWS / Azure VMs
  * VPS providers
  * Containers
  * On-prem servers

➡️ Only the **network location** changes.
The **code and protocol remain the same**.

---

## 🧠 Execution Models in MCP (Quick Recap)

| Model                          | Server Location  | Transport       |
| ------------------------------ | ---------------- | --------------- |
| Local execution                | User machine     | STDIO           |
| Local execution (remote-style) | User machine     | Streamable HTTP |
| Remote execution               | VM / Cloud / VPS | Streamable HTTP |

This lab focuses on the **last two**, using **Streamable HTTP**.

---

## 🔄 Understanding Streamable HTTP in MCP

When using **Streamable HTTP**, communication between the MCP client and server **does not follow the traditional request/response model** used by REST APIs.

### ❌ Traditional Request/Response (REST)

In a typical REST API:

1. Client sends a request
2. Server processes it
3. Server returns **one response**
4. Connection is closed

```
Client → Request → Server
Client ← Response ← Server
(connection ends)
```

Each interaction is isolated.

---

### ✅ Streamed Communication (MCP Streamable HTTP)

With **Streamable HTTP**, the connection remains **open** and acts as a **persistent, bidirectional channel**.

This means:

* The client opens **one HTTP connection**
* The connection stays open
* Multiple MCP messages are exchanged over time
* Both client and server can send messages independently

```
Client ⇄ Server ⇄ Client ⇄ Server
(connection stays open)
```

This is conceptually similar to:

* WebSockets
* Server-Sent Events (SSE)

But implemented in a **firewall-friendly HTTP-based way**.

---

### 🧠 Why MCP Uses Streaming

Streaming is essential because:

* Tool execution may take time
* Results may be incremental
* MCP exchanges multiple message types:

  * Tool calls
  * Tool results
  * Errors
  * Status updates

All of this happens **over the same connection**, enabling:

* Low latency
* Remote execution
* Agent-style interactions
* Real-time orchestration

> ⚠️ Important
> Although HTTP is used, **this is NOT a REST API**.
> HTTP is just the transport; MCP defines its own protocol on top.

---

## 📌 Prerequisites

* Python 3.12+
* UV installed
* MCP CLI available
* Claude Desktop
* Node.js (for `npx`)
* Internet access (for real remote deployments)

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

## 🧑‍💻 Step 5 – Create the MCP Server (`server.py`)

Create a file named `server.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server")

@mcp.tool()
def greeting(name: str) -> str:
    """Send a greeting"""
    return f"Hi {name}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

### Key Line Explained

```python
mcp.run(transport="streamable-http")
```

This tells MCP to:

* Start an HTTP server
* Expose an `/mcp` endpoint
* Accept streamed MCP connections over HTTP

---

## 🔍 Step 6 – Test the Server (Two Terminals)

### 🖥️ Terminal 1 – Run the MCP Server

```bash
mcp run server.py
```

Example output:

```
Serving MCP on http://0.0.0.0:8000
```

The MCP endpoint will be available at:

```
http://0.0.0.0:8000/mcp
```

---

### 🧪 Terminal 2 – Run MCP Inspector

```bash
mcp dev server.py
```

### In the MCP Inspector UI

1. Open the browser
2. Change **Transport Type** to **Streamable HTTP**
3. Set **URL** to:

```
http://0.0.0.0:8000/mcp
```

4. Click **Connect**
5. Go to **Tools**
6. Call the `greeting` tool

✅ If it works, your MCP Server is correctly exposed over HTTP.

---

## 🔌 Step 7 – Enable Claude to Talk to Remote MCP Servers

### ❓ Why an Adapter Is Required

Claude Desktop:

* Only supports **STDIO**
* Cannot connect directly to HTTP MCP Servers

Solution: **`mcp-remote`**

This tool acts as a **bridge**:

```
Claude (STDIO) ⇄ mcp-remote ⇄ HTTP MCP Server
```

---

## 📦 Install `mcp-remote`

```bash
uv add mcp-remote
```

---

## ⚙️ Step 8 – Configure Claude Desktop

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "RemoteServerTest": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://0.0.0.0:8000/mcp/",
        "mcp-server",
        "--allow-http"
      ]
    }
  }
}
```

### What This Configuration Does

* Runs `mcp-remote` locally
* Connects to the MCP Server via HTTP
* Exposes the server to Claude via STDIO

---

## 🔄 Step 9 – Restart Claude Desktop

* Fully **Quit** Claude Desktop
* Reopen it to load the new configuration

---

## 🧪 Step 10 – Test in Claude Desktop

Type:

> **“Send greeting to Gandalf”**

### ✅ Expected Result

```
Hi Gandalf
```

Claude is now communicating with the MCP Server **over HTTP**.

---

## 🌍 From Local to Truly Remote

To make this setup fully remote:

1. Deploy the MCP Server to a VM or container
2. Expose port `8000`
3. Update the URL in Claude’s config
4. Keep the same Streamable HTTP setup

No code changes required.

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* An MCP Server running with Streamable HTTP
* A client communicating over a persistent HTTP connection
* Claude Desktop interacting with a remote MCP Server
* A clear understanding of streamed vs request/response communication

---

## 📌 Key Takeaways

* Streamable HTTP ≠ REST
* MCP uses **persistent HTTP connections**
* Streaming enables remote execution
* `mcp-remote` bridges STDIO and HTTP
* This model supports enterprise and cloud deployments

---

## 📌 Conclusion

This lab completes the MCP execution spectrum:

> **Local execution → Packaged local execution → Remote execution via Streamable HTTP**

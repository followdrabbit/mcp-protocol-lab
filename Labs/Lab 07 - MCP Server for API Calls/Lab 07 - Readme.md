# 🧪 Lab 07 – MCP Server: API Calls (Cryptocurrency Prices)

## 🎯 Lab Objective

In this lab, you will build an **MCP Server that makes external API calls** to retrieve **real-time cryptocurrency prices** using the **CoinGecko public API**.

By the end of this lab, Claude (or any MCP client) will be able to:

* Request cryptocurrency prices (e.g., Bitcoin, Ethereum)
* Trigger an MCP tool that calls a public REST API
* Receive and interpret live market data

This lab introduces **API integration patterns** in MCP Servers.

---

## 🧠 What You Will Learn

* How to call external REST APIs from an MCP Server
* How to expose API-backed logic as MCP tools
* Dependency management and runtime environments in MCP
* Error handling and timeouts in MCP tools
* How MCP enables LLMs to access live, real-world data

---

## ⚠️ Notes on API Usage

* This lab uses the **CoinGecko public API**
* No API key is required
* The API is **rate-limited**
* This implementation is for **learning purposes**, not production-scale usage

---

## 📌 Prerequisites

* Python installed
* UV installed
* Internet access
* Claude Desktop or MCP Inspector (for testing)

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

Install MCP and HTTP client dependencies:

```bash
uv add mcp[cli]
uv add requests
```

### Why these packages?

* **mcp[cli]** → MCP server, client, inspector, installer
* **requests** → HTTP client for REST API calls

---

## 🧑‍💻 Step 5 – Create the MCP Server (`crypto.py`)

Create a file named `crypto.py` with the following content:

```python
from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("Crypto")

@mcp.tool()
def get_cryptocurrency_price(crypto: str) -> str:
    """
    Gets the price of a cryptocurrency.
    Args:
        crypto: symbol of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
    """
    try:
        # Use CoinGecko API to fetch current price in USD
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": crypto.lower(),
            "vs_currencies": "usd"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        price = data.get(crypto.lower(), {}).get("usd")

        if price is not None:
            return f"The price of {crypto} is ${price} USD."
        else:
            return f"Price for {crypto} not found."

    except Exception as e:
        return f"Error fetching price for {crypto}: {e}"

if __name__ == "__main__":
    mcp.run()
```

---

## 🧠 How This MCP Server Works

* Exposes a tool: `get_cryptocurrency_price`
* Makes a real-time HTTP request to CoinGecko
* Parses the JSON response
* Returns live pricing data to the MCP client

This is a **live API-backed MCP Server**.

---

## 🔍 Step 6 – Test with MCP Inspector

Before integrating with Claude, validate the server locally.

```bash
mcp dev crypto.py
```

### In the MCP Inspector Web UI

1. Click **Connect**
2. Go to **Tools**
3. Click **List Tools**
4. Select **get_cryptocurrency_price**
5. Test with:

   * `bitcoin`
   * `ethereum`

### ✅ Expected Result

```
The price of bitcoin is $XXXXX USD.
```

(Actual value will vary.)

---

## 🔌 Step 7 – Install the MCP Server in Claude Desktop

### Option A – Automatic Installation

```bash
mcp install crypto.py
```

⚠️ **Important:**
During testing, this method caused runtime errors related to the `requests` library.

---

## ⚠️ Important Note – Claude Installation & Dependency Resolution

When installing the Crypto MCP Server in Claude, an error occurred because **Claude was not executing the server inside the correct Python environment**, causing the `requests` library to fail at runtime.

### 🧠 Why This Happens

* `mcp install` may register the MCP Server using **system Python**
* Dependencies installed via `uv` are isolated in a virtual environment
* Claude may not automatically activate this environment
* As a result, libraries like `requests` are not found

---

## ✅ Solution – Explicit UV Execution in Claude Configuration

To ensure correct dependency resolution, manually update the Claude MCP configuration.

### 📄 Edit `claude_desktop_config.json`

Add or update the Crypto MCP Server configuration as follows:

```json
{
  "mcpServers": {
    "Crypto": {
      "command": "C:\\Users\\Raphael\\AppData\\Roaming\\Python\\Python312\\Scripts\\uv.EXE",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 07 - MCP Server for API Calls",
        "run",
        "crypto.py"
      ]
    }
  }
}
```

> 🔧 Adjust paths according to your local environment.

---

## 🔄 Step 8 – Restart Claude Desktop

After updating the configuration:

* Fully **Quit** Claude Desktop (use *Quit*, not just close)
* Reopen Claude to load the new MCP Server configuration

---

## 🧪 Step 9 – Test in Claude Desktop

In Claude, try prompts like:

> **“What is the current price of Bitcoin?”**

or

> **“Get the price of Ethereum in USD.”**

### ✅ Expected Behavior

* Claude requests permission to call the **Crypto** MCP Server
* The tool executes using the correct environment
* Claude responds with live pricing data from CoinGecko
* The **Crypto** tool appears in Claude’s connectors/tools panel

---

## 🧩 Troubleshooting

### Price not found

* Use valid CoinGecko IDs (`bitcoin`, not `BTC`)

### Runtime errors

* Ensure Claude uses `uv run`
* Confirm `requests` is installed in the active environment

### Rate limiting

* CoinGecko may temporarily block excessive calls
* Add caching or throttling as a future improvement

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* A working MCP Server that calls an external API
* Correct dependency handling via UV
* Claude Desktop successfully invoking the server
* Live cryptocurrency prices available to an LLM

---

## 📌 Key Takeaways

* MCP Servers often require **explicit runtime control**
* Dependency isolation matters when integrating with Claude
* API-backed MCP tools unlock **real-time intelligence**
* This pattern scales to:

  * Market data
  * Monitoring
  * Risk analysis
  * Financial copilots

---

## 📌 Conclusion

This lab reinforces an essential MCP lesson:

> **Correct execution context is as important as correct code.**

With this fix, your MCP Server is robust, predictable, and production-aligned.

# 🧪 Lab 07 – MCP Server for API Calls (Cryptocurrency Prices)

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
* Error handling and timeouts in MCP tools
* How MCP enables LLMs to access live, real-world data

---

## ⚠️ Notes on API Usage

* This lab uses the **CoinGecko public API**
* No API key is required
* The API is **rate-limited**
* This implementation is for **learning purposes**, not high-scale production use

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
* **requests** → Simple HTTP client for REST API calls

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

1. The tool `get_cryptocurrency_price` is exposed via MCP
2. When called:

   * It sends an HTTP request to CoinGecko
   * Parses the JSON response
   * Extracts the USD price
3. The result is returned as plain text to the MCP client

This is a **live API-backed MCP tool**.

---

## 🔍 Step 6 – Test with MCP Inspector

Before integrating with Claude, validate the server locally.

### ▶️ Start MCP Inspector

```bash
mcp dev crypto.py
```

### 🌐 In the MCP Inspector Web UI

1. Click **Connect**
2. Go to **Tools**
3. Click **List Tools**
4. Select **get_cryptocurrency_price**
5. Provide a value, for example:

   * `bitcoin`
   * `ethereum`
6. Click **Run Tool**

### ✅ Expected Result

Example output:

```
The price of bitcoin is $65432 USD.
```

(Actual value will vary.)

---

## 🔌 Step 7 – Install the MCP Server in Claude Desktop

Install the server so Claude can invoke it:

```bash
mcp install crypto.py
```

If your server depends on a virtual environment (recommended), ensure Claude uses `uv run` as shown in previous labs.

---

## 🔄 Step 8 – Restart Claude Desktop

* Fully **Quit** Claude Desktop (do not just close the window)
* Reopen the application to load the new MCP Server

---

## 🧪 Step 9 – Test in Claude Desktop

In Claude, try prompts like:

> **“What is the current price of Bitcoin?”**

or

> **“Get the price of Ethereum in USD.”**

### ✅ Expected Behavior

* Claude requests permission to call the **Crypto** MCP Server
* The `get_cryptocurrency_price` tool is executed
* Claude responds with live price data from CoinGecko

You should also see the **Crypto** tool listed in Claude’s connectors/tools panel.

---

## 🧩 Troubleshooting

### API returns an error

* Ensure you are using valid CoinGecko IDs (`bitcoin`, not `BTC`)
* Check internet connectivity

### Rate limits

* CoinGecko may temporarily block excessive requests
* Add caching or throttling in future versions

### Claude can’t execute the server

* Ensure the MCP Server is executed with `uv run`
* Verify `requests` is installed in the correct virtual environment

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* An MCP Server that calls an external API
* A tool that returns live cryptocurrency prices
* A working integration between MCP, APIs, and LLMs

---

## 📌 Key Takeaways

* MCP Servers can safely expose **live external data**
* REST APIs integrate naturally as MCP tools
* This pattern is foundational for:

  * Market data assistants
  * Monitoring dashboards
  * Financial analysis copilots
  * Risk and pricing engines

---

## 📌 Conclusion

This lab demonstrates how MCP extends LLM capabilities beyond static knowledge by integrating **real-time APIs**.

You now have MCP examples covering:

* Local state (files)
* OS interaction (screenshots)
* Remote services (APIs)
* External data sources (crypto markets)

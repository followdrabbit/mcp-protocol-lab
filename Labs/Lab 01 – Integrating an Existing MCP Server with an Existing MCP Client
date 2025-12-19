# 🧪 Lab 01 – Integrating an Existing MCP Server with an Existing MCP Client

## 🎯 Lab Objective

The goal of this lab is to **integrate an existing MCP Server** with an **existing MCP Client**, using:

* **Claude Desktop** as the MCP Host and MCP Client
* **Airbnb MCP Server** as the MCP Server

You will validate the integration by comparing Claude’s behavior **before and after** the MCP configuration.

---

## 🧠 Architecture Overview

* **MCP Client / Host:** Claude Desktop
* **MCP Server:** Airbnb MCP Server
* **Execution model:** On-demand via `npx`
* **Integration type:** Local configuration (`claude_desktop_config.json`)

---

## 📌 Prerequisites

* Claude Desktop installed
* Node.js and NPM installed
* Internet access
* Permission to edit local configuration files

---

## 🔗 Repositories Used

* MCP Organization: [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
* MCP Servers List: [https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
* Airbnb MCP Server: [https://github.com/openbnb-org/mcp-server-airbnb](https://github.com/openbnb-org/mcp-server-airbnb)

---

## 🧪 Step 0 – Baseline Test (Before MCP Configuration)

Before configuring any MCP Server, test Claude’s default behavior.

### 🔍 Test Question

Ask Claude Desktop:

> **“Find me Airbnb in Paris”**

### 📝 Expected Behavior (Before MCP)

* Claude responds using **general knowledge only**
* No external data source is called
* No tools or connectors are triggered
* Results are generic and not sourced from Airbnb

This establishes a **baseline** for comparison.

---

## 🛠️ Method 1 – Script-Based Integration (npx)

This method configures Claude Desktop to automatically start the Airbnb MCP Server whenever Airbnb-related context is required.

---

### 📄 MCP Server Configuration (Airbnb)

In the Airbnb MCP Server repository, locate the section:

> **“To ignore robots.txt for all requests, use this version with `--ignore-robots-txt` args”**

Copy the configuration below:

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

---

### ⚙️ Configuring Claude Desktop

1. Open **Claude Desktop**
2. Navigate to:

   ```
   File → Settings
   ```
3. Open the **Developer** section
4. Click **“Edit config”**
5. When the file selector opens, right-click:

   ```
   claude_desktop_config.json
   ```
6. Open it with a text editor

> ⚠️ Note
> The file will be empty the first time.

7. Paste the MCP configuration
8. Save the file

---

### 🔄 Restarting Claude Desktop

* Fully close Claude Desktop by selecting **“Quit”** from the menu
* Simply closing the window is not sufficient

📌 Note:
If Claude Desktop fails to reopen after the change, **restart your computer**.
After reboot, the MCP configuration should load correctly.

---

## 🧪 Step 1 – Validation Test (After MCP Configuration)

After restarting Claude Desktop, repeat the same question.

### 🔍 Test Question

> **“Find me Airbnb in Paris”**

---

### 🧠 Expected Behavior (After MCP)

After the configuration:

1. **Claude will ask for authorization**

   * A prompt appears requesting permission to call the **Airbnb MCP Server**

2. Once authorized:

   * Claude executes the MCP Server command:

     ```bash
     npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt
     ```

3. Claude’s response now:

   * Uses **real-time or structured Airbnb data**
   * Is enriched with MCP-provided context
   * Is no longer purely generic

---

### 🔌 Visual Confirmation in Claude

You can confirm the integration in two ways:

* **Authorization prompt** when Claude first calls the MCP
* **Airbnb MCP tool appears in Claude’s Connectors / Tools list**

This confirms that:

* The MCP Server is registered
* Claude can invoke it on demand

---

## 🔍 How This Integration Works

* Claude Desktop monitors user prompts
* When a prompt matches Airbnb-related intent:

  * Claude selects the Airbnb MCP Server
  * Executes it locally via `npx`
  * Injects the server’s response as structured context

The server is **not always running** — it is started **only when needed**.

---

## ✅ Expected Outcome

* Clear behavioral difference before vs. after MCP configuration
* Claude requests authorization to call the Airbnb MCP Server
* Airbnb MCP tool is visible in Claude connectors
* Airbnb-related answers are contextually enriched

---

## 📌 Conclusion

This lab demonstrates how MCP enables:

* Declarative, zero-code integration
* Safe, permission-based tool execution
* Context-aware enrichment of LLM responses

It also introduces a **repeatable validation pattern** that will be reused in future labs.

# MCP Protocol Lab

📚 Central repository for studying, experimenting, and documenting the **Model Context Protocol (MCP)**.

---

## 🎯 Objectives
- Understand MCP concepts and architecture
- Explore message flows and protocol fundamentals
- Build hands-on labs and experiments
- Document security, scalability, and integration considerations
- Create reusable references and examples

---

## 📂 Repository Structure

```text
.
├── docs/        # Conceptual documentation and study notes
├── labs/        # Hands-on labs and practical experiments
├── examples/    # Minimal working examples
├── references/  # Articles, specs, and external resources
└── README.md
```

---

## 🧰 Requirements and Setup

To get the most out of the course and successfully run the hands-on labs, the following tools, accounts, and configurations are required.

### 🔧 Development Tools

* **Visual Studio Code (VS Code)**
  Used to edit lab source code.
  Includes free integration with **GitHub Copilot**, which can act as an **MCP client** by connecting to MCP servers.

* **Python**
  Primary language used to implement labs and MCP servers.

* **Claude Desktop**
  Used as an **MCP Host** and **MCP Client** to test and interact with the MCP servers created throughout the labs.

* **UV**
  Fast and modern Python dependency and environment manager.
  👉 [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

* **Node.js / NPM**
  Required for MCP SDKs, tooling, and JavaScript-based integrations.

---

### ☁️ Accounts and Credentials

* **OpenAI API Key**
  Used in selected labs for LLM integration and context-based experiments.

* **GitHub Account**
  Required for source control and for deploying **MCP servers online**, using GitHub as the deployment and automation manager.

* **Azure Portal Account**
  Used to deploy **remote MCP servers** and explore cloud-based hosting and integration scenarios.

---

## 🧠 Topics Covered

* MCP fundamentals
* Context management
* Message formats and flows
* Client ↔ Server interactions
* Security and trust boundaries
* Context isolation and data exposure risks
* Integration and deployment patterns

---

## 🚀 Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/mcp-protocol-lab.git
   ```

2. Install required tools:

   * VS Code
   * Python
   * Node.js / NPM
   * UV
   * Claude Desktop

3. Configure credentials:

   * OpenAI API Key
   * GitHub account access
   * Azure Portal access

4. Start with the `docs/` directory to understand MCP fundamentals.

5. Proceed to `labs/` to run hands-on experiments and build MCP servers.

---

## 🔐 Security Perspective

This project approaches MCP with a strong **security and architecture mindset**, covering:

* Trust boundaries between MCP clients and servers
* Secure context handling
* Minimization of data exposure
* Deployment considerations in cloud environments

---

## 📌 Disclaimer

This repository is intended for **educational and experimental purposes only** and does not represent an official MCP specification or endorsement.
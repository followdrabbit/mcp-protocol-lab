# 🧪 Lab 09 – MCP Server: Custom Schema Inputs (Pydantic)

## 🎯 Lab Objective

In this lab, you will build an **MCP Server that uses custom structured inputs** defined with **Pydantic schemas**.

Instead of accepting raw strings, your MCP tool will receive a **validated object** with multiple fields, enabling safer, more reliable, and more expressive interactions with LLMs.

By the end of this lab, Claude will be able to:

* Parse natural language into a structured schema
* Call an MCP tool with typed inputs
* Persist structured data into a local file

---

## 🧠 Why Custom Schemas Matter

Using schemas brings several benefits:

* Strong **input validation**
* Clear contracts between LLM and tool
* Better UX in MCP Inspector (form-like fields)
* Reduced hallucinations and malformed inputs
* Production-ready patterns for real systems

---

## 📌 Prerequisites

* Python installed
* UV installed
* MCP CLI available
* VS Code (recommended)
* Claude Desktop (for final integration)

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
* Confirms environment is active

---

## 📦 Step 4 – Install Required Packages

```bash
uv add mcp[cli]
uv add pydantic
```

> ℹ️ Note
> `openai` is **not required** in this lab because the server does not call an external LLM API.

---

## 🧑‍💻 Step 5 – Create the MCP Server (`other_inputs.py`)

Create `other_inputs.py` with the following content:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List

# Create server
mcp = FastMCP("Other Inputs")

class Person(BaseModel):
    first_name: str = Field(..., description="The person's first name")
    last_name: str = Field(..., description="The person's last name")
    years_of_experience: int = Field(..., description="Number of years of experience")
    previous_addresses: List[str] = Field(
        default_factory=list,
        description="List of previous addresses"
    )


@mcp.tool()
def add_person_to_member_database(person: Person) -> str:
    """
    Logs the personal details of the given person to the database.
    """

    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"First Name: {person.first_name}\n")
        log_file.write(f"Last Name: {person.last_name}\n")
        log_file.write(f"Years of Experience: {person.years_of_experience}\n")
        log_file.write("Previous Addresses:\n")
        for idx, address in enumerate(person.previous_addresses, 1):
            log_file.write(f"  {idx}. {address}\n")
        log_file.write("\n")

    return "Data has been logged"


if __name__ == "__main__":
    mcp.run()
```

---

## 📄 Step 6 – Create the Log File

Create an empty file:

```text
log.txt
```

This file will store structured entries written by the MCP tool.

---

## 🔍 Step 7 – Test with MCP Inspector

Run the Inspector:

```bash
mcp dev other_inputs.py
```

### In the MCP Inspector UI

1. Click **Connect**
2. Go to **Tools**
3. Click **List Tools**
4. Open **add_person_to_member_database**

You will see structured fields generated from the `Person` schema.

### Example Test Input

* `first_name`: `Gandalfa`
* `last_name`: `TheGrey`
* `years_of_experience`: `900`
* `previous_addresses`:

  * `Narnia`
  * `Isengard`

Click **Run Tool**.

### ✅ Expected Result

* Response:

  ```
  Data has been logged
  ```
* Data appears in `log.txt`

---

## 🔌 Step 8 – Install the MCP Server in Claude Desktop

### Option A – Automatic Installation

```bash
mcp install other_inputs.py
```

⚠️ **Important:**
As observed in previous labs, this may fail due to **virtual environment resolution issues**.

---

## ⚠️ Important Note – Claude Runtime Configuration (Required Fix)

During testing, Claude failed to execute the MCP Server correctly because it was **not running inside the UV-managed environment**, causing dependency resolution issues.

### 🧠 Why This Happens

* `mcp install` may use **system Python**
* Dependencies live inside `.venv`
* Claude does not automatically activate the environment
* Result: runtime failures or missing libraries

---

## ✅ Solution – Explicit `uv run` Configuration in Claude

Manually edit Claude’s configuration file.

### 📄 Update `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "Other Inputs": {
      "command": "C:\\Users\\Raphael\\AppData\\Roaming\\Python\\Python312\\Scripts\\uv.EXE",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 09  MCP Server for Custom Schema Inputs",
        "run",
        "other_inputs.py"
      ]
    }
  }
}
```

> 🔧 Adjust paths according to your local environment.

---

## 🔄 Step 9 – Restart Claude Desktop

* Fully **Quit** Claude Desktop (do not just close)
* Reopen Claude to load the updated configuration

---

## 🧪 Step 10 – Test in Claude Desktop

Use the prompt:

> **“Log the following person to db: Gandalfa, 900 years of experience, he has previously lived in Narnia and Isengard.”**

### ✅ Expected Behavior

* Claude requests permission to call **Other Inputs**
* Claude converts text into a structured `Person` object
* MCP tool writes structured data to `log.txt`
* Claude confirms successful execution

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* An MCP Server using **custom typed inputs**
* A validated schema enforced by Pydantic
* Successful execution via Claude Desktop
* Reliable structured data persistence

---

## 📌 Key Takeaways

* MCP supports **strongly typed tool inputs**
* Schemas improve safety, reliability, and UX
* Claude can infer and populate structured objects
* This pattern is ideal for:

  * Forms
  * Onboarding flows
  * Incident reports
  * Risk assessments
  * Enterprise workflows

## 📌 Conclusion

This lab demonstrates how MCP supports **strongly typed tool inputs** — moving from “string prompts” to **validated, structured data**.

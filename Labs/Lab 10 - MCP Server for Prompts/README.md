# 🧪 Lab 10 – MCP Server for Prompts

## 🎯 Lab Objective

In this lab, you will create an **MCP Server that exposes primitive prompts** instead of tools.

Primitive prompts allow MCP to:

* Provide **predefined prompt templates**
* Let the user (or Claude) inject parameters
* Reuse high-quality prompts consistently
* Separate **prompt engineering** from execution logic

By the end of this lab, Claude will be able to:

* List available prompts
* Fill prompt parameters via UI
* Inject prompts directly into the conversation

---

## 🧠 What Are MCP Prompts?

Unlike MCP **tools**, which *execute logic*, MCP **prompts**:

* Return **prompt text only**
* Do not perform actions
* Are injected into the conversation context
* Act as **prompt templates**

Think of them as:

* Reusable prompt snippets
* Prompt-as-a-service
* Prompt libraries exposed via MCP

---

## 📌 Prerequisites

* Python installed
* UV installed
* MCP CLI available
* Claude Desktop (for prompt integration testing)

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
* Confirms the environment is active

---

## 📦 Step 4 – Install Required Packages

```bash
uv add mcp[cli]
```

> ℹ️ No additional libraries are required.
> This lab focuses purely on MCP prompt primitives.

---

## 🧑‍💻 Step 5 – Create the MCP Server (`prompt.py`)

Create a file named `prompt.py` with the following content:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Prompt")

@mcp.prompt()
def get_prompt(topic: str) -> str:
    """
    Returns a prompt that performs a detailed analysis on a topic.
    Args:
        topic: the topic to analyze
    """
    return f"Do a detailed analysis on the following topic: {topic}"


@mcp.prompt()
def write_detailed_historical_report(topic: str, number_of_paragraphs: int) -> str:
    """
    Writes a detailed historical report.
    Args:
        topic: the topic to research
        number_of_paragraphs: number of paragraphs in the main section
    """

    prompt = """
Create a concise research report on the history of {topic}.

The report should contain 3 sections:
1. INTRODUCTION
2. MAIN
3. CONCLUSION

Requirements:
- The MAIN section must have {number_of_paragraphs} paragraphs
- Include a timeline of key events
- The CONCLUSION must be written in bullet points
"""

    return prompt.format(
        topic=topic,
        number_of_paragraphs=number_of_paragraphs
    )


if __name__ == "__main__":
    mcp.run()
```

---

## 🧠 How This MCP Server Works

* Uses `@mcp.prompt()` instead of `@mcp.tool()`
* Each function returns **pure prompt text**
* Claude injects the returned prompt into the conversation
* No code execution or side effects occur

---

## 🔍 Step 6 – Test with MCP Inspector

Run the MCP Inspector:

```bash
mcp dev prompt.py
```

### In the MCP Inspector UI

1. Click **Connect**
2. Go to **Prompts**
3. Click **List Prompts**
4. Test:

   * `get_prompt`
   * `write_detailed_historical_report`

You will see input fields generated from the function parameters.

---

## 🔌 Step 7 – Install the MCP Server in Claude Desktop

### Option A – Automatic Installation

```bash
mcp install prompt.py
```

⚠️ As seen in previous labs, this may fail if Claude does not use the correct runtime environment.

---

## ⚠️ Important Note – Claude Runtime Configuration

If Claude fails to load the prompts, configure the MCP Server explicitly using `uv run`.

### ✅ Correct `claude_desktop_config.json` Entry

> 🔴 **Correction applied:**
> Your original snippet referenced **Lab 09 and `other_inputs.py`**, which is incorrect for this lab.

Use the following **correct configuration**:

```json
{
  "mcpServers": {
    "Prompt": {
      "command": "C:\\Users\\Raphael\\AppData\\Roaming\\Python\\Python312\\Scripts\\uv.EXE",
      "args": [
        "--directory",
        "C:\\Users\\Raphael\\repos\\mcp-protocol-lab\\Labs\\Lab 10 - MCP Server for Prompts",
        "run",
        "prompt.py"
      ]
    }
  }
}
```

> 🔧 Adjust paths according to your local environment.

---

## 🔄 Step 8 – Restart Claude Desktop

* Fully **Quit** Claude Desktop (not just close)
* Reopen Claude so the new MCP Server is loaded

---

## 🧪 Step 9 – Test Prompt Integration in Claude

### Method 1 – Prompt Picker (UI)

1. Click the **“+”** icon in Claude
2. Select **Add Prompts**
3. Choose `get_prompt`
4. Enter a topic (e.g., *Artificial Intelligence*)
5. Click **Add Prompt**

Claude will inject the generated prompt into the conversation.

---

### Method 2 – Multi-Parameter Prompt

1. Click **Add Prompts**
2. Choose `write_detailed_historical_report`
3. Example inputs:

   * `topic`: *Roman Empire*
   * `number_of_paragraphs`: `4`
4. Add the prompt

Claude will continue the conversation using the injected structured prompt.

---

## ✅ Expected Outcome

By the end of this lab, you will have:

* An MCP Server exposing **prompt primitives**
* Parameterized prompt templates
* Prompts accessible directly from Claude’s UI
* Clean separation between prompt design and execution

---

## 📌 Key Takeaways

* MCP prompts are **first-class primitives**
* They enable reusable, high-quality prompt engineering
* Prompts are safer than tools when no execution is required
* Ideal for:

  * Research templates
  * Writing assistants
  * Analysis frameworks
  * Standardized reports

---

## 📌 Conclusion

This lab completes a critical MCP capability:

> **Treating prompts as reusable, versioned, and centrally managed artifacts.**
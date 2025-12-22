from __future__ import annotations

import os

from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis do .\.env (na mesma pasta do script / diretório atual)
load_dotenv(dotenv_path=".env")

# Ex.: no seu .env coloque:
# PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "PERPLEXITY_API_KEY não encontrada no arquivo .env. "
        "Crie um .env na mesma pasta e adicione: PERPLEXITY_API_KEY=..."
    )

mcp = FastMCP("Web Search")

@mcp.tool()
def perform_websearch(query: str) -> str:
    """
    Performs a web search for a query
    Args:
        query: the query to web search.
    """
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that searches the web and responds to questions",
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )

    return response.choices[0].message.content


def main():
    # Recomendo forçar stdio no Claude/inspector
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

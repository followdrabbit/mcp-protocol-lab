"""
Memories MCP Server (LAB)
-------------------------

Este servidor MCP expõe ferramentas para:
- salvar "memórias" em um Vector Store (RAG),
- buscar memórias por similaridade semântica,
- listar, obter conteúdo e apagar memórias.

Boas práticas aplicadas:
- Evita stdout (importante em MCP via stdio).
- Usa BytesIO (sem arquivos temporários no disco).
- Adiciona metadata (attributes) para filtragem.
- Cache do vector_store_id para evitar listagens repetidas.
- Validações + redaction opcional de segredos (chaves, tokens).
"""

from __future__ import annotations

import io
import os
import re
import sys
import json
import time
import hashlib
import logging
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from openai import OpenAI
from mcp.server.fastmcp import FastMCP


# ============================================================================
# Logging (IMPORTANTE: MCP stdio => não usar stdout)
# ----------------------------------------------------------------------------
# - stdout é usado pelo protocolo MCP quando você roda em stdio.
# - então logs devem ir para stderr.
# ============================================================================
logger = logging.getLogger("memories_mcp")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
_handler = logging.StreamHandler(sys.stderr)
_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(_handler)


# ============================================================================
# Configuração via .env / env vars
# ============================================================================
load_dotenv()

# Nome padrão do Vector Store (pode mudar via env)
VECTOR_STORE_NAME = os.getenv("MEMORIES_VECTOR_STORE_NAME", "MEMORIES_STORE")

# Opcional: se você já sabe o ID do store, setar isso evita listagem/scan
VECTOR_STORE_ID_ENV = os.getenv("MEMORIES_VECTOR_STORE_ID")

# Limite simples pra evitar uploads gigantes no lab
MAX_MEMORY_CHARS = int(os.getenv("MEMORIES_MAX_CHARS", "8000"))

# Redaction default ON (mais seguro para “memórias” de conversas)
REDACT_SECRETS_DEFAULT = os.getenv("MEMORIES_REDACT_SECRETS", "true").lower() == "true"

# Cliente OpenAI (pega OPENAI_API_KEY do ambiente automaticamente)
client = OpenAI()


# ============================================================================
# MCP Server
# ============================================================================
mcp = FastMCP("Memories")


# ============================================================================
# Cache do Vector Store
# ----------------------------------------------------------------------------
# Evita chamar list() a cada tool call. Em ambientes reais, você pode persistir
# esse ID num config/DB.
# ============================================================================
_vector_store_id_cache: Optional[str] = VECTOR_STORE_ID_ENV or None
_vector_store_lock = threading.Lock()


def _utc_now_iso() -> str:
    """Retorna timestamp ISO em UTC (útil para metadata)."""
    return datetime.now(timezone.utc).isoformat()


def _sha256_text(text: str) -> str:
    """Hash simples para deduplicação / rastreio."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ============================================================================
# Redaction (opcional)
# ----------------------------------------------------------------------------
# Não é “DLP perfeito”, mas ajuda a não salvar acidentalmente:
# - chaves (OpenAI, AWS, etc),
# - tokens Bearer,
# - strings tipo "api_key=..."
# ============================================================================
_SECRET_PATTERNS = [
    # Bearer tokens
    re.compile(r"(?i)\bAuthorization:\s*Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9\-\._~\+\/]+=*\b"),
    # AWS Access Key ID (heurístico)
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    # Strings comuns de api keys
    re.compile(r"(?i)\b(openai|api)[-_ ]?key\b\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"(?i)\btoken\b\s*[:=]\s*['\"]?[^'\"\s]+"),
]


def _redact_secrets(text: str) -> str:
    """Substitui padrões de segredo por [REDACTED]."""
    redacted = text
    for pat in _SECRET_PATTERNS:
        redacted = pat.sub("[REDACTED]", redacted)
    return redacted


# ============================================================================
# Vector Store helpers
# ============================================================================
def _get_or_create_vector_store_id() -> str:
    """
    Retorna o vector_store_id.
    - Se já estiver em cache/env, usa direto.
    - Senão, procura por nome e cria caso não exista.

    OBS: list() pode ser paginado; aqui mantemos simples para lab, mas já
    suportamos paginação básica por "after".
    """
    global _vector_store_id_cache

    # Fast path: cache já preenchido
    if _vector_store_id_cache:
        return _vector_store_id_cache

    with _vector_store_lock:
        # Double-check dentro do lock
        if _vector_store_id_cache:
            return _vector_store_id_cache

        logger.info("Vector store id não está em cache. Procurando/criando...")

        # Paginação básica
        after: Optional[str] = None
        while True:
            page = client.vector_stores.list(limit=100, after=after)  # limit 1..100
            for store in page.data:
                if store.name == VECTOR_STORE_NAME:
                    _vector_store_id_cache = store.id
                    logger.info(f"Encontrado vector store existente: {store.id}")
                    return store.id

            if not getattr(page, "has_more", False):
                break

            after = getattr(page, "last_id", None)
            if not after:
                break

        # Se não achou, cria
        created = client.vector_stores.create(name=VECTOR_STORE_NAME)
        _vector_store_id_cache = created.id
        logger.info(f"Criado novo vector store: {created.id}")
        return created.id


def _upload_text_as_file_to_vector_store(
    vector_store_id: str,
    text: str,
    filename: str,
) -> str:
    """
    Faz upload do texto para o vector store como "arquivo" e retorna file_id.

    - Usamos BytesIO para não escrever em disco.
    - upload_and_poll espera um file-like object.
    """
    bio = io.BytesIO(text.encode("utf-8"))
    # Alguns SDKs dependem do atributo .name para nomear corretamente
    bio.name = filename  # type: ignore[attr-defined]

    # upload_and_poll retorna um "vector_store.file" object (id = file_id)
    vs_file = client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store_id,
        file=bio,
    )
    return vs_file.id


def _update_vector_store_file_attributes(
    vector_store_id: str,
    file_id: str,
    attributes: Dict[str, Union[str, int, float, bool]],
) -> None:
    """
    Atualiza attributes do arquivo dentro do vector store.

    Limites (conforme docs):
    - até 16 pares key-value
    - keys até 64 chars
    - values até 512 chars (strings) ou bool/number
    """
    # “attributes” é suportado por update no endpoint de vector store files
    client.vector_stores.files.update(
        vector_store_id=vector_store_id,
        file_id=file_id,
        attributes=attributes,
    )


# ============================================================================
# Filtros para busca (attributes filtering)
# ----------------------------------------------------------------------------
# A doc mostra exemplos de comparação e composições (and/or). :contentReference[oaicite:2]{index=2}
# Nota: em algumas partes aparece "attribute_filter", em outras "filters".
# Aqui aceitamos "attribute_filter" do usuário, e tentamos enviar como
# "filters" primeiro; se falhar, tentamos "attribute_filter".
# ============================================================================
AttributeFilter = Dict[str, Any]


def _build_attribute_filter(
    user_id: Optional[str],
    session_id: Optional[str],
    tags: Optional[List[str]],
    memory_type: Optional[str],
) -> Optional[AttributeFilter]:
    """
    Cria um filtro composto (AND) usando os atributos que existirem.
    """
    filters: List[AttributeFilter] = []

    if user_id:
        filters.append({"type": "eq", "key": "user_id", "value": user_id})
    if session_id:
        filters.append({"type": "eq", "key": "session_id", "value": session_id})
    if memory_type:
        filters.append({"type": "eq", "key": "type", "value": memory_type})
    if tags:
        # Exemplo simples: exige que "tags_json" seja exatamente a mesma string.
        # Em produção, você pode modelar tags em campos separados (tag_1, tag_2, etc)
        # ou criar uma convenção para filtros "contains" (se/quando suportado).
        filters.append({"type": "eq", "key": "tags_json", "value": json.dumps(tags, ensure_ascii=False)})

    if not filters:
        return None

    if len(filters) == 1:
        return filters[0]

    return {"type": "and", "filters": filters}


# ============================================================================
# MCP Tools
# ============================================================================
@mcp.tool()
def health() -> Dict[str, Any]:
    """
    Healthcheck simples do servidor.
    Útil para validar se:
    - chave está configurada,
    - MCP está rodando.
    """
    return {
        "status": "ok",
        "vector_store_name": VECTOR_STORE_NAME,
        "vector_store_id_cached": bool(_vector_store_id_cache),
        "time_utc": _utc_now_iso(),
    }


@mcp.tool()
def save_memory(
    memory: str,
    user_id: str = "default",
    session_id: Optional[str] = None,
    memory_type: str = "note",
    tags: Optional[List[str]] = None,
    redact_secrets: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Salva uma "memória" no vector store.

    Parâmetros:
    - memory: texto a ser salvo
    - user_id: útil pra separar memórias por usuário (default "default")
    - session_id: útil pra separar por sessão/conversa (opcional)
    - memory_type: categoria simples (ex: note, preference, decision, todo...)
    - tags: lista de tags (opcional)
    - redact_secrets: se True, faz redaction de segredos antes de salvar

    Retorna:
    - file_id, sha256, vector_store_id
    """
    if not isinstance(memory, str) or not memory.strip():
        return {"status": "error", "error": "memory deve ser uma string não-vazia"}

    if len(memory) > MAX_MEMORY_CHARS:
        return {
            "status": "error",
            "error": f"memory excede o limite do lab ({MAX_MEMORY_CHARS} chars).",
        }

    do_redact = REDACT_SECRETS_DEFAULT if redact_secrets is None else bool(redact_secrets)
    cleaned = _redact_secrets(memory) if do_redact else memory

    vector_store_id = _get_or_create_vector_store_id()

    # Hash do conteúdo (útil pra dedupe/rastreabilidade)
    mem_hash = _sha256_text(cleaned)

    # Nome “bonitinho” para o arquivo (facilita debug)
    ts = int(time.time())
    safe_user = re.sub(r"[^a-zA-Z0-9_\-]", "_", user_id)[:32]
    filename = f"memory_{safe_user}_{ts}.txt"

    try:
        # 1) Upload do conteúdo
        file_id = _upload_text_as_file_to_vector_store(
            vector_store_id=vector_store_id,
            text=cleaned,
            filename=filename,
        )

        # 2) Attributes (metadata) — até 16 campos (mantenha curto!)
        attributes: Dict[str, Union[str, int, float, bool]] = {
            "user_id": user_id[:64],
            "type": memory_type[:64],
            "timestamp_utc": _utc_now_iso()[:64],
            "sha256": mem_hash[:64],
            "redacted": bool(do_redact),
        }

        if session_id:
            attributes["session_id"] = session_id[:64]

        if tags:
            # Como o filtro é por igualdade, serializamos como JSON estável
            attributes["tags_json"] = json.dumps(tags, ensure_ascii=False)[:512]

        # Atualiza attributes
        _update_vector_store_file_attributes(
            vector_store_id=vector_store_id,
            file_id=file_id,
            attributes=attributes,
        )

        return {
            "status": "saved",
            "vector_store_id": vector_store_id,
            "file_id": file_id,
            "sha256": mem_hash,
            "attributes": attributes,
        }

    except Exception as e:
        logger.exception("Falha ao salvar memória")
        return {"status": "error", "error": str(e)}


@mcp.tool()
def search_memory(
    query: str,
    user_id: str = "default",
    session_id: Optional[str] = None,
    memory_type: Optional[str] = None,
    tags: Optional[List[str]] = None,
    max_results: int = 8,
    rewrite_query: bool = True,
    return_full_items: bool = False,
) -> Dict[str, Any]:
    """
    Busca memórias por similaridade semântica.

    Parâmetros:
    - query: texto de busca
    - user_id/session_id/memory_type/tags: filtros por attributes (opcionais)
    - max_results: 1..50 (o serviço limita)
    - rewrite_query: melhora recall em muitos casos
    - return_full_items: se True, retorna itens com score/filename/attributes

    Retorna:
    - results: lista de textos (default) OU lista de objetos completos
    """
    if not isinstance(query, str) or not query.strip():
        return {"status": "error", "error": "query deve ser uma string não-vazia"}

    # Bound do max_results para o limite aceito (1..50)
    max_results = max(1, min(int(max_results), 50))

    vector_store_id = _get_or_create_vector_store_id()

    attribute_filter = _build_attribute_filter(
        user_id=user_id,
        session_id=session_id,
        tags=tags,
        memory_type=memory_type,
    )

    # ----------------------------------------------------------------------------
    # Observação importante:
    # - API ref usa "filters" (file attributes filter)
    # - Em alguns guias aparece "attribute_filter"
    # Para o LAB, fazemos fallback automático.
    # ----------------------------------------------------------------------------
    try:
        # Tenta com "filters" (API reference)
        results = client.vector_stores.search(
            vector_store_id=vector_store_id,
            query=query,
            max_num_results=max_results,
            rewrite_query=rewrite_query,
            filters=attribute_filter,
        )
    except TypeError:
        # Fallback para variação de nome em alguns SDKs/versões
        results = client.vector_stores.search(
            vector_store_id=vector_store_id,
            query=query,
            max_num_results=max_results,
            rewrite_query=rewrite_query,
            attribute_filter=attribute_filter,
        )

    # O retorno vem com:
    # - search_query (pode vir reescrita)
    # - data: lista com (file_id, filename, score, attributes, content[])
    if return_full_items:
        full_items: List[Dict[str, Any]] = []
        for item in results.data:
            texts = [c.text for c in item.content if getattr(c, "type", None) == "text"]
            full_items.append(
                {
                    "file_id": item.file_id,
                    "filename": item.filename,
                    "score": item.score,
                    "attributes": getattr(item, "attributes", None),
                    "content_texts": texts,
                }
            )
        return {
            "status": "ok",
            "vector_store_id": vector_store_id,
            "search_query": getattr(results, "search_query", query),
            "results": full_items,
            "has_more": getattr(results, "has_more", False),
        }

    # Default: só os chunks de texto (bem simples para o lab)
    content_texts = [
        c.text
        for item in results.data
        for c in item.content
        if getattr(c, "type", None) == "text"
    ]

    return {
        "status": "ok",
        "vector_store_id": vector_store_id,
        "search_query": getattr(results, "search_query", query),
        "results": content_texts,
        "has_more": getattr(results, "has_more", False),
    }


@mcp.tool()
def list_memories(
    user_id: Optional[str] = None,
    limit: int = 20,
    status_filter: Optional[str] = "completed",
) -> Dict[str, Any]:
    """
    Lista arquivos no vector store (útil para debug/admin do lab).

    Parâmetros:
    - user_id: se fornecido, filtra localmente (client-side) por attributes.user_id
      (o endpoint list não filtra por attributes, então é pós-filtro).
    - limit: 1..100 por página
    - status_filter: in_progress | completed | failed | cancelled (ou None)
    """
    vector_store_id = _get_or_create_vector_store_id()
    limit = max(1, min(int(limit), 100))

    page = client.vector_stores.files.list(
        vector_store_id=vector_store_id,
        limit=limit,
        filter=status_filter,
        order="desc",
    )

    # Para listar attributes, precisamos retrieve() de cada file (lab: ok).
    items: List[Dict[str, Any]] = []
    for f in page.data:
        detail = client.vector_stores.files.retrieve(vector_store_id=vector_store_id, file_id=f.id)
        attrs = getattr(detail, "attributes", None) or {}
        if user_id and attrs.get("user_id") != user_id:
            continue
        items.append(
            {
                "file_id": detail.id,
                "created_at": getattr(detail, "created_at", None),
                "status": getattr(detail, "status", None),
                "attributes": attrs,
            }
        )

    return {
        "status": "ok",
        "vector_store_id": vector_store_id,
        "count": len(items),
        "items": items,
        "has_more": getattr(page, "has_more", False),
        "last_id": getattr(page, "last_id", None),
    }


@mcp.tool()
def get_memory_content(file_id: str) -> Dict[str, Any]:
    """
    Recupera o conteúdo parseado de um arquivo do vector store.

    OBS:
    - O endpoint existe (GET .../content).
    - Dependendo da versão do SDK, o método pode ser .content(...) ou outro.
    Aqui tentamos o método mais provável e, se falhar, devolvemos um erro claro.
    """
    vector_store_id = _get_or_create_vector_store_id()

    # Primeiro pega metadata/attributes
    detail = client.vector_stores.files.retrieve(vector_store_id=vector_store_id, file_id=file_id)
    attrs = getattr(detail, "attributes", None) or {}

    # Agora tenta pegar o conteúdo parseado
    try:
        content_obj = client.vector_stores.files.content(
            vector_store_id=vector_store_id,
            file_id=file_id,
        )
        # content_obj.content deve ser uma lista de chunks {type,text,...}
        texts = [c.get("text") for c in content_obj.get("content", []) if c.get("type") == "text"]
        return {
            "status": "ok",
            "vector_store_id": vector_store_id,
            "file_id": file_id,
            "attributes": attrs,
            "content_texts": [t for t in texts if t],
        }

    except AttributeError:
        # Se o SDK não expõe .content, você pode:
        # - atualizar o SDK
        # - ou usar request HTTP direto (fora do escopo do lab)
        return {
            "status": "error",
            "error": "Seu openai SDK não expõe client.vector_stores.files.content(...). Atualize o pacote openai.",
            "vector_store_id": vector_store_id,
            "file_id": file_id,
            "attributes": attrs,
        }
    except Exception as e:
        logger.exception("Falha ao obter conteúdo")
        return {"status": "error", "error": str(e), "vector_store_id": vector_store_id, "file_id": file_id}


@mcp.tool()
def delete_memory(file_id: str) -> Dict[str, Any]:
    """
    Remove um arquivo do vector store (não deleta o 'File' global, apenas desanexa do store).
    """
    vector_store_id = _get_or_create_vector_store_id()
    try:
        deleted = client.vector_stores.files.delete(
            vector_store_id=vector_store_id,
            file_id=file_id,
        )
        return {
            "status": "ok",
            "vector_store_id": vector_store_id,
            "file_id": file_id,
            "deleted": getattr(deleted, "deleted", True),
        }
    except Exception as e:
        logger.exception("Falha ao deletar memória")
        return {"status": "error", "error": str(e), "vector_store_id": vector_store_id, "file_id": file_id}


# ============================================================================
# Main
# ============================================================================
if __name__ == "__main__":
    # MCP stdio server
    # Dica: rode com logs em stderr, e evite prints em stdout.
    mcp.run(transport="stdio")

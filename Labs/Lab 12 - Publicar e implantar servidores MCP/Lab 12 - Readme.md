# Lab 12 — Publicar e implantar servidores MCP (empacotamento e distribuição)

## Objetivo do lab

Criar servidor MCP, empacotar e implantar no github, criar um script json para instalar o pacote na maquina local e rodar o servidor que criamos localmente.

## Introdução

A distribuição de um servidor MCP que ocorre de duas formas:

### 1. **Pacote NPM + execução local via `npx`** (modelo “Airbnb MCP”)

#### Modelo mental do fluxo

1. Você configura o cliente com um comando (ex.: `npx ...`).
2. O **Host** executa o comando e **sobe um processo local** (Node).
3. O **Host** manda `ListTools` → o server responde com as tools disponíveis.
4. Quando precisa, o **Host** manda `CallTool` → o server executa e responde.

✅ Ponto-chave: nesse modelo, **o servidor não precisa abrir porta nem rodar como webservice**. Ele vive como um processo local.

#### Exemplo real (Airbnb MCP)

Configuração típica no cliente:

```json
{
  "mcpServers": {
    "airbnb": {
      "command": "npx",
      "args": ["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
    }
  }
}
```

Equivalente no terminal:

```bash
npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt
```

### O que esse comando faz (em termos de empacotamento)

* `npx` baixa o pacote do NPM
* executa o **binário** definido no `package.json` do pacote
* o bin aponta para um arquivo compilado (normalmente `dist/index.js`)
* o processo inicia um Server MCP e conecta via **stdio** (stdin/stdout)

### 2. **Servidor rodando remotamente** (VM/Container) e cliente configurado para conectar

#### Quando faz sentido

* você quer centralizar controle (rate-limit, auth, auditoria)
* você não quer que o usuário baixe/execute nada local
* você quer atualizar sem depender de update do cliente

#### O que muda

Em vez de `npx ...` rodando local, você hospeda o servidor e o cliente:

* conecta via um transporte de rede (depende da stack do servidor e do host)
* exige preocupações adicionais: autenticação, TLS, logs, disponibilidade, custo



#!/usr/bin/env python3
# =============================================================================
# Trabalho 2 - Redes de Computadores 2
# Exercício 10: Chat em Rede com WebSockets - SERVIDOR
#
# Integrantes do grupo:
#   - NOME DO INTEGRANTE 1
#   - NOME DO INTEGRANTE 2
#   - NOME DO INTEGRANTE 3
#
# Descrição:
#   Servidor de chat usando a biblioteca 'websockets' (asyncio). Aceita
#   múltiplas conexões simultâneas e retransmite (broadcast) cada mensagem
#   recebida para os demais clientes, identificando o remetente pelo nome.
#
# Protocolo (mensagens JSON):
#   Cliente -> servidor:
#     {"tipo": "entrar",   "nome": "ana"}      primeira mensagem obrigatória
#     {"tipo": "mensagem", "texto": "olá"}     mensagens de chat
#   Servidor -> cliente:
#     {"tipo": "mensagem", "nome": "ana", "texto": "olá", "hora": "14:05:31"}
#     {"tipo": "sistema",  "texto": "ana entrou na sala.", "hora": "..."}
#     {"tipo": "erro",     "texto": "Nome já em uso."}
# =============================================================================

import argparse
import asyncio
import json
from datetime import datetime

import websockets
from websockets.exceptions import ConnectionClosed

# Mapeia cada conexão WebSocket ativa para o nome do usuário.
# Como o asyncio roda em uma única thread, não é necessário Lock.
clientes: dict = {}

TAM_MAX_NOME = 20
TAM_MAX_MSG = 1000


def hora() -> str:
    return datetime.now().strftime("%H:%M:%S")


def log(texto: str) -> None:
    """Imprime uma linha de log no console do servidor com data/hora."""
    print(f"[{datetime.now():%d/%m/%Y %H:%M:%S}] {texto}", flush=True)


async def enviar(ws, dados: dict) -> None:
    """Envia um dicionário como JSON, ignorando conexões que já caíram."""
    try:
        await ws.send(json.dumps(dados, ensure_ascii=False))
    except ConnectionClosed:
        pass


async def broadcast(dados: dict, exceto=None) -> None:
    """Envia 'dados' a todos os clientes conectados, exceto 'exceto'."""
    destinos = [ws for ws in list(clientes) if ws is not exceto]
    # Envia para todos em paralelo; falhas individuais não afetam os outros.
    await asyncio.gather(*(enviar(ws, dados) for ws in destinos))


def validar_nome(nome) -> str | None:
    """Retorna uma mensagem de erro se o nome for inválido, ou None se ok."""
    if not isinstance(nome, str) or not nome.strip():
        return "O nome de usuário não pode ser vazio."
    if len(nome.strip()) > TAM_MAX_NOME:
        return f"O nome deve ter no máximo {TAM_MAX_NOME} caracteres."
    if nome.strip().lower() in (n.lower() for n in clientes.values()):
        return "Este nome já está em uso. Escolha outro."
    return None


async def atender(ws) -> None:
    """Corrotina executada para cada cliente conectado."""
    endereco = f"{ws.remote_address[0]}:{ws.remote_address[1]}" if ws.remote_address else "?"
    nome = None
    try:
        # ---- Etapa 1: identificação do usuário ------------------------------
        async for bruto in ws:
            try:
                msg = json.loads(bruto)
            except (json.JSONDecodeError, TypeError):
                await enviar(ws, {"tipo": "erro", "texto": "Mensagem inválida (JSON esperado)."})
                continue
            if not isinstance(msg, dict) or msg.get("tipo") != "entrar":
                await enviar(ws, {"tipo": "erro", "texto": "Informe seu nome primeiro."})
                continue
            erro = validar_nome(msg.get("nome"))
            if erro:
                await enviar(ws, {"tipo": "erro", "texto": erro})
                continue
            nome = msg["nome"].strip()
            break
        if nome is None:          # desconectou antes de se identificar
            return

        clientes[ws] = nome
        log(f"{nome} ({endereco}) entrou. Online: {len(clientes)}")
        await enviar(ws, {"tipo": "sistema", "hora": hora(),
                          "texto": f"Bem-vindo(a), {nome}! Online: "
                                   f"{', '.join(clientes.values())}"})
        await broadcast({"tipo": "sistema", "hora": hora(),
                         "texto": f"{nome} entrou na sala."}, exceto=ws)

        # ---- Etapa 2: laço de mensagens -------------------------------------
        async for bruto in ws:
            try:
                msg = json.loads(bruto)
            except (json.JSONDecodeError, TypeError):
                continue                       # ignora lixo sem derrubar nada
            if not isinstance(msg, dict) or msg.get("tipo") != "mensagem":
                continue
            texto = str(msg.get("texto", "")).strip()
            if not texto:
                continue                       # ignora mensagens vazias
            texto = texto[:TAM_MAX_MSG]
            log(f"{nome}: {texto}")
            await broadcast({"tipo": "mensagem", "nome": nome,
                             "texto": texto, "hora": hora()}, exceto=ws)

    except ConnectionClosed:
        # Desconexão inesperada (aba fechada, queda de rede, Ctrl+C no cliente).
        pass
    finally:
        # Sempre remove o cliente e avisa os demais, seja saída normal ou abrupta.
        if nome is not None and clientes.pop(ws, None) is not None:
            log(f"{nome} ({endereco}) saiu. Online: {len(clientes)}")
            await broadcast({"tipo": "sistema", "hora": hora(),
                             "texto": f"{nome} saiu da sala."})


async def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor de chat com WebSockets")
    parser.add_argument("--host", default="0.0.0.0",
                        help="endereço de escuta (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=8765,
                        help="porta de escuta (padrão: 8765)")
    args = parser.parse_args()

    if not 1 <= args.porta <= 65535:
        parser.error("a porta deve estar entre 1 e 65535")

    try:
        async with websockets.serve(atender, args.host, args.porta):
            log(f"Servidor WebSocket em ws://{args.host}:{args.porta} (Ctrl+C para encerrar)")
            await asyncio.Future()        # mantém o servidor rodando para sempre
    except OSError as erro:
        print(f"Erro ao abrir a porta {args.porta}: {erro}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Servidor encerrado.")

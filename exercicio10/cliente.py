#!/usr/bin/env python3
# =============================================================================
# Trabalho 2 - Redes de Computadores 2
# Exercício 10: Chat em Rede com WebSockets - CLIENTE (terminal)
#
# Integrantes do grupo:
#   - NOME DO INTEGRANTE 1
#   - NOME DO INTEGRANTE 2
#   - NOME DO INTEGRANTE 3
#
# Descrição:
#   Cliente de chat em Python usando a biblioteca 'websockets'. Duas tarefas
#   asyncio rodam em paralelo: uma lê o teclado e envia mensagens, a outra
#   recebe e exibe as mensagens do servidor em tempo real.
#   Digite "sair" para encerrar.
# =============================================================================

import argparse
import asyncio
import json
import os
import sys

import websockets
from websockets.exceptions import ConnectionClosed

COMANDO_SAIR = "sair"


def exibir(msg: dict) -> None:
    """Formata e imprime uma mensagem recebida do servidor."""
    tipo = msg.get("tipo")
    if tipo == "mensagem":
        print(f"[{msg.get('hora')}] {msg.get('nome')}: {msg.get('texto')}", flush=True)
    elif tipo == "sistema":
        print(f"[{msg.get('hora')}] *** {msg.get('texto')} ***", flush=True)
    elif tipo == "erro":
        print(f"[ERRO] {msg.get('texto')}", flush=True)


async def receber(ws) -> None:
    """Tarefa de leitura: imprime tudo o que chega do servidor."""
    try:
        async for bruto in ws:
            try:
                exibir(json.loads(bruto))
            except json.JSONDecodeError:
                print(bruto)
    except ConnectionClosed:
        pass
    print("\n[Conexão encerrada pelo servidor]")


async def entrar(ws) -> str | None:
    """Pede um nome ao usuário até o servidor aceitá-lo."""
    while True:
        nome = (await asyncio.to_thread(input, "Digite seu nome de usuário: ")).strip()
        if not nome:
            print("O nome não pode ser vazio.")
            continue
        await ws.send(json.dumps({"tipo": "entrar", "nome": nome}))
        resposta = json.loads(await ws.recv())
        exibir(resposta)
        if resposta.get("tipo") != "erro":
            return nome


async def enviar(ws) -> None:
    """Tarefa de escrita: lê o teclado sem bloquear o laço de eventos."""
    while True:
        # readline() é bloqueante; to_thread o executa fora do laço do asyncio.
        texto = await asyncio.to_thread(sys.stdin.readline)
        if not texto:                       # EOF (Ctrl+D)
            return
        texto = texto.strip()
        if not texto:
            continue                        # não envia mensagens vazias
        if texto.lower() == COMANDO_SAIR:
            return
        await ws.send(json.dumps({"tipo": "mensagem", "texto": texto}))


async def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente de chat WebSocket")
    parser.add_argument("--host", default="127.0.0.1",
                        help="endereço do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=8765,
                        help="porta do servidor (padrão: 8765)")
    args = parser.parse_args()
    uri = f"ws://{args.host}:{args.porta}"

    try:
        async with websockets.connect(uri) as ws:
            await entrar(ws)
            print(f"Conectado a {uri}. Digite '{COMANDO_SAIR}' para sair.")
            tarefa_rx = asyncio.create_task(receber(ws))
            tarefa_tx = asyncio.create_task(enviar(ws))
            # Termina quando o usuário sai OU o servidor cai.
            _, pendentes = await asyncio.wait({tarefa_rx, tarefa_tx},
                                              return_when=asyncio.FIRST_COMPLETED)
            for t in pendentes:
                t.cancel()
    except (ConnectionRefusedError, OSError):
        print(f"Não foi possível conectar: servidor {uri} indisponível.")
        sys.exit(1)
    except ConnectionClosed:
        print("Conexão encerrada.")
    print("Desconectado.")
    # Encerra mesmo se a thread do teclado ainda estiver aguardando um Enter.
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nDesconectado.")

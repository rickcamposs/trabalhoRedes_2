#!/usr/bin/env python3
# =============================================================================
# Trabalho 2 - Redes de Computadores 2
# Exercício 3: Chat em Rede (TCP) - CLIENTE
#
# Integrantes do grupo:
#   - NOME DO INTEGRANTE 1
#   - NOME DO INTEGRANTE 2
#   - NOME DO INTEGRANTE 3
#
# Descrição:
#   Cliente de chat TCP. Usa duas linhas de execução:
#     - a thread principal lê o teclado e envia as mensagens ao servidor;
#     - uma thread secundária recebe continuamente as mensagens do servidor
#       e as exibe na tela.
#   Assim o usuário pode enviar e receber mensagens ao mesmo tempo.
# =============================================================================

import argparse
import socket
import sys
import threading

COMANDO_SAIR = "sair"

# Evento usado para sinalizar entre as threads que a conexão terminou.
encerrado = threading.Event()
# Evento que indica que foi o próprio usuário quem pediu para sair.
saindo = threading.Event()


def receber_mensagens(sock: socket.socket) -> None:
    """Thread de leitura: recebe dados do servidor e imprime cada linha."""
    buffer = b""
    try:
        while not encerrado.is_set():
            dados = sock.recv(1024)
            if not dados:                 # servidor fechou a conexão
                break
            buffer += dados
            # O TCP é um fluxo de bytes; separamos as mensagens pelo '\n'.
            while b"\n" in buffer:
                linha, buffer = buffer.split(b"\n", 1)
                print(linha.decode("utf-8", errors="replace"), flush=True)
    except OSError:
        pass                              # socket fechado pela thread principal
    finally:
        if not encerrado.is_set() and not saindo.is_set():
            print("\n[Conexão encerrada pelo servidor. Pressione Enter para sair.]")
        encerrado.set()


def enviar(sock: socket.socket, texto: str) -> bool:
    """Envia uma linha ao servidor. Retorna False se a conexão caiu."""
    try:
        sock.sendall((texto + "\n").encode("utf-8"))
        return True
    except OSError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente de chat TCP")
    parser.add_argument("--host", default="127.0.0.1",
                        help="endereço do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=5000,
                        help="porta do servidor (padrão: 5000)")
    args = parser.parse_args()

    # Solicita o nickname antes de conectar, validando entrada vazia.
    try:
        nick = ""
        while not nick:
            nick = input("Digite seu nickname: ").strip()
            if not nick:
                print("O nickname não pode ser vazio.")
    except (EOFError, KeyboardInterrupt):
        print()
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((args.host, args.porta))
    except ConnectionRefusedError:
        print(f"Não foi possível conectar: servidor {args.host}:{args.porta} indisponível.")
        sock.close()
        sys.exit(1)
    except OSError as erro:
        print(f"Erro ao conectar: {erro}")
        sock.close()
        sys.exit(1)

    # Inicia a thread que recebe mensagens em paralelo com a digitação.
    leitor = threading.Thread(target=receber_mensagens, args=(sock,), daemon=True)
    leitor.start()

    try:
        enviar(sock, nick)    # primeira linha do protocolo: o nickname
        # Laço principal: lê o teclado e envia ao servidor.
        while not encerrado.is_set():
            texto = input()
            if encerrado.is_set():
                break
            if not texto.strip():
                continue                  # não envia mensagens vazias
            if texto.strip().lower() == COMANDO_SAIR:
                saindo.set()
            if not enviar(sock, texto):
                print("[Falha ao enviar: conexão perdida]")
                break
            if texto.strip().lower() == COMANDO_SAIR:
                leitor.join(timeout=2)    # espera a despedida do servidor
                break
    except (EOFError, KeyboardInterrupt):
        saindo.set()
        enviar(sock, COMANDO_SAIR)        # Ctrl+C/Ctrl+D também saem de forma limpa
    finally:
        encerrado.set()
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()
        print("Desconectado.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# =============================================================================
# Trabalho 2 - Redes de Computadores 2
# Exercício 3: Chat em Rede (TCP) - SERVIDOR
#
# Integrantes do grupo:
#   - NOME DO INTEGRANTE 1
#   - NOME DO INTEGRANTE 2
#   - NOME DO INTEGRANTE 3
#
# Descrição:
#   Servidor de chat TCP multithread. Cada cliente conectado é atendido por
#   uma thread própria. Toda mensagem recebida de um cliente é retransmitida
#   (broadcast) para os demais, precedida do nickname do remetente. Entradas
#   e saídas de usuários são notificadas a todos os participantes.
#
# Protocolo (texto UTF-8, uma mensagem por linha terminada em '\n'):
#   1. A primeira linha enviada pelo cliente é o seu nickname.
#   2. As linhas seguintes são mensagens de chat.
#   3. A linha "sair" encerra a sessão do cliente.
# =============================================================================

import argparse
import socket
import threading
from datetime import datetime

# Dicionário compartilhado entre as threads: socket do cliente -> nickname.
clientes: dict[socket.socket, str] = {}
# Lock que protege o acesso concorrente ao dicionário 'clientes'.
clientes_lock = threading.Lock()

TAM_MAX_NICK = 20       # tamanho máximo permitido para o nickname
COMANDO_SAIR = "sair"   # comando que encerra a sessão do cliente


def log(texto: str) -> None:
    """Imprime uma linha de log no console do servidor com data/hora."""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{agora}] {texto}", flush=True)


def enviar_linha(sock: socket.socket, texto: str) -> bool:
    """Envia uma linha de texto para um socket. Retorna False em caso de erro."""
    try:
        sock.sendall((texto + "\n").encode("utf-8"))
        return True
    except OSError:
        return False


def broadcast(texto: str, remetente: socket.socket | None = None) -> None:
    """
    Envia 'texto' para todos os clientes conectados, exceto o remetente.
    Clientes cujo envio falhar são removidos da lista (conexão perdida).
    """
    # Copia a lista sob o lock para não segurá-lo durante operações de rede.
    with clientes_lock:
        destinos = [s for s in clientes if s is not remetente]

    falhos = [s for s in destinos if not enviar_linha(s, texto)]

    # Remove clientes cuja conexão caiu durante o envio.
    if falhos:
        with clientes_lock:
            for s in falhos:
                clientes.pop(s, None)


def ler_linhas(sock: socket.socket):
    """
    Gerador que lê dados do socket e devolve uma linha por vez.
    Necessário porque o TCP é um fluxo de bytes: uma chamada recv() pode
    trazer meia mensagem ou várias mensagens juntas.
    """
    buffer = b""
    while True:
        dados = sock.recv(1024)
        if not dados:            # recv() vazio = cliente fechou a conexão
            return
        buffer += dados
        while b"\n" in buffer:
            linha, buffer = buffer.split(b"\n", 1)
            yield linha.decode("utf-8", errors="replace").strip()


def nickname_em_uso(nick: str) -> bool:
    """Verifica (de forma thread-safe) se o nickname já está em uso."""
    with clientes_lock:
        return nick.lower() in (n.lower() for n in clientes.values())


def atender_cliente(conn: socket.socket, endereco: tuple) -> None:
    """Função executada por uma thread para cada cliente conectado."""
    ip_porta = f"{endereco[0]}:{endereco[1]}"
    nick = None
    try:
        linhas = ler_linhas(conn)

        # ---- Etapa 1: negociação do nickname --------------------------------
        for linha in linhas:
            if not linha:
                enviar_linha(conn, "[SERVIDOR] Nickname vazio. Digite outro:")
            elif len(linha) > TAM_MAX_NICK:
                enviar_linha(conn, f"[SERVIDOR] Nickname deve ter no máximo "
                                   f"{TAM_MAX_NICK} caracteres. Digite outro:")
            elif linha.lower() == COMANDO_SAIR:
                return
            elif nickname_em_uso(linha):
                enviar_linha(conn, "[SERVIDOR] Nickname já em uso. Digite outro:")
            else:
                nick = linha
                break
        if nick is None:          # cliente desconectou antes de escolher nick
            return

        with clientes_lock:
            clientes[conn] = nick
            total = len(clientes)

        log(f"{nick} ({ip_porta}) entrou. Usuários online: {total}")
        enviar_linha(conn, f"[SERVIDOR] Bem-vindo(a), {nick}! "
                           f"Usuários online: {total}. Digite '{COMANDO_SAIR}' para sair.")
        broadcast(f"[SERVIDOR] {nick} entrou na sala.", remetente=conn)

        # ---- Etapa 2: laço de mensagens -------------------------------------
        for linha in linhas:
            if not linha:                     # ignora mensagens vazias
                continue
            if linha.lower() == COMANDO_SAIR:
                enviar_linha(conn, "[SERVIDOR] Até logo!")
                break
            log(f"{nick} ({ip_porta}): {linha}")
            broadcast(f"{nick}: {linha}", remetente=conn)

    except (ConnectionResetError, BrokenPipeError, OSError) as erro:
        # Queda abrupta do cliente: não deve derrubar o servidor.
        log(f"Conexão com {nick or ip_porta} perdida: {erro}")
    finally:
        # Remove o cliente da lista e avisa os demais participantes.
        with clientes_lock:
            estava_na_sala = clientes.pop(conn, None) is not None
            total = len(clientes)
        conn.close()
        if nick and estava_na_sala:
            log(f"{nick} ({ip_porta}) saiu. Usuários online: {total}")
            broadcast(f"[SERVIDOR] {nick} saiu da sala.")
        elif not nick:
            log(f"{ip_porta} desconectou sem entrar na sala.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor de chat TCP multithread")
    parser.add_argument("--host", default="0.0.0.0",
                        help="endereço de escuta (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=5000,
                        help="porta de escuta (padrão: 5000)")
    args = parser.parse_args()

    if not 1 <= args.porta <= 65535:
        parser.error("a porta deve estar entre 1 e 65535")

    # Socket TCP (SOCK_STREAM) sobre IPv4 (AF_INET).
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        # Permite reutilizar a porta logo após reiniciar o servidor.
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            servidor.bind((args.host, args.porta))
        except OSError as erro:
            print(f"Erro ao abrir a porta {args.porta}: {erro}")
            return
        servidor.listen()
        log(f"Servidor de chat escutando em {args.host}:{args.porta} (Ctrl+C para encerrar)")

        try:
            while True:
                conn, endereco = servidor.accept()
                log(f"Nova conexão de {endereco[0]}:{endereco[1]}")
                # Uma thread por cliente; daemon=True para encerrar junto com o servidor.
                threading.Thread(target=atender_cliente, args=(conn, endereco),
                                 daemon=True).start()
        except KeyboardInterrupt:
            log("Encerrando servidor...")
            broadcast("[SERVIDOR] O servidor está sendo encerrado.")
            with clientes_lock:
                for s in list(clientes):
                    s.close()


if __name__ == "__main__":
    main()

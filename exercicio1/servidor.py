"""
Exercício 1 - Servidor TCP multithread
Integrantes: Felipe Veloso,Gabriel Moraes, Riquelme Campos
"""
import argparse
import socket
import threading
from datetime import datetime


def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def atender_cliente(conn, addr):
    """Roda em uma thread: cuida de UM cliente até ele sair."""
    ip, porta = addr
    print(f"[{agora()}] Conectado: {ip}:{porta}")
    try:
        with conn:
            while True:
                dados = conn.recv(1024)
                if not dados:
                    break
                msg = dados.decode("utf-8", errors="replace").strip()
                print(f"[{agora()}] {ip}:{porta} -> {msg}")
                conn.sendall("Mensagem recebida".encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError):
        print(f"[{agora()}] Conexão perdida com {ip}:{porta}")
    finally:
        print(f"[{agora()}] Desconectado: {ip}:{porta}")


def main():
    parser = argparse.ArgumentParser(description="Servidor TCP multithread")
    parser.add_argument("--host", default="0.0.0.0", help="Endereço (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=5000, help="Porta (padrão: 5000)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((args.host, args.porta))
        servidor.listen()
        print(f"Servidor ouvindo em {args.host}:{args.porta} (Ctrl+C para parar)")
        try:
            while True:
                conn, addr = servidor.accept()
                t = threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    main()

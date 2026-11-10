"""
Exercício 4 - Servidor de hora multithread
Integrantes: Felipe Veloso, Gabriel Moraes, Riquelme Campos
"""
import argparse
import socket
import threading
from datetime import datetime

contador = 0
lock = threading.Lock()


def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def atender_cliente(conn, addr):
    global contador
    ip, porta = addr
    try:
        with conn:
            conn.settimeout(10)
            conn.recv(1024)
            hora = datetime.now().strftime("%H:%M:%S")
            conn.sendall(hora.encode("utf-8"))
            with lock:
                contador += 1
                atual = contador
            print(f"[{agora()}] Cliente {ip}:{porta} atendido | Total atendidos: {atual}")
    except Exception as e:
        print(f"[{agora()}] Erro com {ip}:{porta}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Servidor de hora")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--porta", type=int, default=7000)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((args.host, args.porta))
        servidor.listen()
        print(f"Servidor de hora em {args.host}:{args.porta} (Ctrl+C para parar)")
        try:
            while True:
                conn, addr = servidor.accept()
                print(f"[{agora()}] Solicitação recebida de {addr[0]}:{addr[1]}")
                threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    main()

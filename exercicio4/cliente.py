"""
Exercício 4 - Cliente do servidor de hora
Integrantes: Felipe Veloso, Gabriel Moraes, Riquelme Campos
"""
import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="Cliente do servidor de hora")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--porta", type=int, default=7000)
    args = parser.parse_args()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((args.host, args.porta))
            s.sendall(b"HORA")
            hora = s.recv(1024).decode("utf-8")
            print("Hora do servidor:", hora)
    except ConnectionRefusedError:
        print("Erro: servidor indisponível.")
    except socket.timeout:
        print("Erro: o servidor não respondeu a tempo.")


if __name__ == "__main__":
    main()

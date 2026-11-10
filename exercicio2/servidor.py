"""
Exercício 2 - Servidor Echo UDP
Integrantes: Felipe Veloso, Gabriel Moraes, Riquelme Campos
"""
import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="Servidor Echo UDP")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--porta", type=int, default=6000)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((args.host, args.porta))
        print(f"Servidor UDP em {args.host}:{args.porta} (Ctrl+C para parar)")
        try:
            while True:
                dados, addr = s.recvfrom(65535)
                print(f"{addr[0]}:{addr[1]} -> {dados.decode('utf-8', errors='replace')}")
                s.sendto(dados, addr)
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    main()

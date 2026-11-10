"""
Exercício 2 - Cliente Echo UDP
Integrantes: Felipe Veloso, Gabriel Moraes, Riquelme Campos
"""
import argparse
import socket

MAX_UDP = 65507


def main():
    parser = argparse.ArgumentParser(description="Cliente Echo UDP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--porta", type=int, default=6000)
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(args.timeout)
        print("Digite 'sair' para encerrar.")
        try:
            while True:
                msg = input("Mensagem: ").strip()
                if not msg:
                    print("Mensagem vazia não é permitida.")
                    continue
                if msg.lower() == "sair":
                    break
                dados = msg.encode("utf-8")
                if len(dados) > MAX_UDP:
                    print(f"Mensagem grande demais ({len(dados)} bytes). Máximo: {MAX_UDP}.")
                    continue
                try:
                    s.sendto(dados, (args.host, args.porta))
                    eco, _ = s.recvfrom(65535)
                    print("Eco:", eco.decode("utf-8", errors="replace"))
                except socket.timeout:
                    print("Tempo esgotado: sem resposta do servidor.")
                except OSError as e:
                    print(f"Erro de comunicação: {e}")
        except KeyboardInterrupt:
            print("\nEncerrado.")


if __name__ == "__main__":
    main()

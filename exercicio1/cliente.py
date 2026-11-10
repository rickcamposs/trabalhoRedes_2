"""
Exercício 1 - Cliente TCP
Integrantes: Felipe Veloso, Gabriel Moraes, Riquelme Campos
"""
import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="Cliente TCP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--porta", type=int, default=5000)
    args = parser.parse_args()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((args.host, args.porta))
            print(f"Conectado a {args.host}:{args.porta}. Digite 'sair' para encerrar.")
            while True:
                msg = input("Mensagem: ").strip()
                if not msg:
                    print("Mensagem vazia não é permitida.")
                    continue
                if msg.lower() == "sair":
                    break
                s.sendall(msg.encode("utf-8"))
                resposta = s.recv(1024)
                if not resposta:
                    print("O servidor encerrou a conexão.")
                    break
                print("Servidor:", resposta.decode("utf-8"))
    except ConnectionRefusedError:
        print("Erro: servidor indisponível. Ele está rodando nessa porta?")
    except KeyboardInterrupt:
        print("\nEncerrado.")


if __name__ == "__main__":
    main()

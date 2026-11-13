# Exercício 1 - Cliente-Servidor TCP

## Integrantes do grupo

- Felipe Alcântara Guimarães Veloso
- Gabriel de Jesus Moraes Maurício
- Riquelme Moreira Campos

## Requisitos
Python 3.10+ (somente biblioteca padrão, nada a instalar).

## Como executar
Terminal 1 (servidor):
    python3 servidor.py --porta 5000
Terminal 2 (cliente):
    python3 cliente.py --host 127.0.0.1 --porta 5000

## Parâmetros
--host: endereço (cliente padrão 127.0.0.1; servidor padrão 0.0.0.0)
--porta: porta TCP (padrão 5000)

## Uso
Digite mensagens e pressione Enter. Digite "sair" para encerrar o cliente.

# Exercício 2 - Servidor Echo UDP

## Integrantes do grupo

- Felipe Alcântara Guimarães Veloso
- Gabriel de Jesus Moraes Maurício
- Riquelme Moreira Campos

## Requisitos
Python 3.10+ (somente biblioteca padrão).

## Como executar
Terminal 1 (servidor):
    python3 servidor.py --porta 6000
Terminal 2 (cliente):
    python3 cliente.py --host 127.0.0.1 --porta 6000 --timeout 3

## Parâmetros
--host, --porta (padrão 6000), --timeout em segundos (cliente, padrão 3)

## Uso
Digite mensagens e Enter; o servidor devolve o eco. "sair" encerra. Tamanho máximo: 65.507 bytes.

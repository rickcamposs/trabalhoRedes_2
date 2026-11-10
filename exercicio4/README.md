# Exercício 4 - Servidor de Hora com Threads

Integrantes: Nome 1, Nome 2, Nome 3

## Requisitos
Python 3.10+ (somente biblioteca padrão).

## Como executar
Terminal 1 (servidor):
    python3 servidor.py --porta 7000
Terminal 2 (cliente, pode repetir várias vezes):
    python3 cliente.py --host 127.0.0.1 --porta 7000

## Parâmetros
--host, --porta (padrão 7000)

## Funcionamento
O cliente conecta, solicita e exibe a hora (HH:MM:SS). O servidor registra cada
atendimento com data/hora, cliente e contador total (protegido por threading.Lock).

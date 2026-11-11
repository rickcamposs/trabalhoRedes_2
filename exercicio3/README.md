# Exercício 3 — Chat em Rede (TCP)

Chat em tempo real com um servidor central TCP multithread e vários clientes.

## Requisitos

- Linux
- Python 3.10 ou superior
- Nenhuma biblioteca externa (apenas a biblioteca padrão: `socket`, `threading`, `argparse`)

## Como executar

**1. Inicie o servidor** (em um terminal):

```bash
python3 servidor.py --porta 5000
```

Parâmetros opcionais:

| Parâmetro | Padrão    | Descrição                |
|-----------|-----------|--------------------------|
| `--host`  | `0.0.0.0` | Endereço de escuta       |
| `--porta` | `5000`    | Porta TCP de escuta      |

**2. Inicie quantos clientes quiser** (um terminal para cada):

```bash
python3 cliente.py --host 127.0.0.1 --porta 5000
```

| Parâmetro | Padrão      | Descrição             |
|-----------|-------------|-----------------------|
| `--host`  | `127.0.0.1` | Endereço do servidor  |
| `--porta` | `5000`      | Porta do servidor     |

Ao abrir, o cliente pede um **nickname**. Depois disso, basta digitar as mensagens e pressionar Enter.
Digite **`sair`** para encerrar o cliente (o servidor e os demais clientes continuam funcionando).
Para encerrar o servidor, use `Ctrl+C`.

## Funcionamento

- **Servidor:** cria uma thread para cada cliente aceito. A lista de clientes é compartilhada entre as threads e protegida por um `threading.Lock`. Cada mensagem recebida é retransmitida (broadcast) a todos os outros clientes no formato `nickname: mensagem`. Entradas e saídas são avisadas a todos com `[SERVIDOR] fulano entrou/saiu da sala.`
- **Cliente:** a thread principal lê o teclado e envia; uma segunda thread fica lendo o socket continuamente e imprimindo o que chega, o que permite enviar e receber ao mesmo tempo.
- **Protocolo:** texto UTF-8, uma mensagem por linha (`\n`). Como o TCP é um fluxo de bytes, os dois lados acumulam os dados recebidos em um buffer e separam as mensagens pelo `\n`. A primeira linha enviada pelo cliente é o nickname.

## Tratamento de erros

- Nickname vazio, longo demais (> 20 caracteres) ou já em uso é recusado e o servidor pede outro.
- Mensagens vazias são ignoradas.
- Servidor indisponível (conexão recusada) gera mensagem amigável no cliente.
- Queda abrupta de um cliente (terminal fechado, `Ctrl+C`, rede) é detectada, o cliente é removido e os demais são notificados, sem derrubar o servidor.
- Porta inválida ou já em uso é informada ao iniciar o servidor.

## Exemplo de uso

```
# Terminal do cliente "ana"
Digite seu nickname: ana
[SERVIDOR] Bem-vindo(a), ana! Usuários online: 1. Digite 'sair' para sair.
[SERVIDOR] bruno entrou na sala.
bruno: oi ana!
olá bruno
[SERVIDOR] bruno saiu da sala.
```

# Exercício 10 — Chat em Rede com WebSockets

## Integrantes do grupo

- Felipe Alcântara Guimarães Veloso
- Gabriel de Jesus Moraes Maurício
- Riquelme Moreira Campos

Chat em tempo real com servidor em Python (biblioteca `websockets`) e dois clientes possíveis: um de terminal em Python e uma página HTML que usa a WebSocket API nativa do navegador. Os dois clientes podem conversar entre si na mesma sala.

## Requisitos

- Linux
- Python 3.10 ou superior
- Biblioteca `websockets` (testado com a versão 17.4):

```bash
pip install -r requirements.txt
# ou: pip install websockets
```

## Como executar

**1. Inicie o servidor:**

```bash
python3 servidor.py --porta 8765
```

| Parâmetro | Padrão    | Descrição           |
|-----------|-----------|---------------------|
| `--host`  | `0.0.0.0` | Endereço de escuta  |
| `--porta` | `8765`    | Porta de escuta     |

**2a. Cliente de terminal (Python)** — abra um terminal para cada usuário:

```bash
python3 cliente.py --host 127.0.0.1 --porta 8765
```

O cliente pede o nome de usuário; depois é só digitar as mensagens. Digite **`sair`** para encerrar.

**2b. Cliente no navegador (HTML/JavaScript)** — abra o arquivo diretamente:

```bash
xdg-open cliente.html
```

Confira o endereço do servidor (padrão `ws://localhost:8765`), digite seu nome e clique em **Entrar**. Abra o arquivo em várias abas para simular vários usuários.

Para encerrar o servidor, use `Ctrl+C`.

## Protocolo

As mensagens trafegam em JSON:

| Direção            | Exemplo                                                                  |
|--------------------|--------------------------------------------------------------------------|
| cliente → servidor | `{"tipo": "entrar", "nome": "ana"}` (primeira mensagem, obrigatória)     |
| cliente → servidor | `{"tipo": "mensagem", "texto": "olá"}`                                   |
| servidor → cliente | `{"tipo": "mensagem", "nome": "ana", "texto": "olá", "hora": "14:05:31"}`|
| servidor → cliente | `{"tipo": "sistema", "texto": "ana entrou na sala.", "hora": "..."}`     |
| servidor → cliente | `{"tipo": "erro", "texto": "Este nome já está em uso. Escolha outro."}`  |

## Funcionamento

- O servidor usa `asyncio`: cada conexão é atendida por uma corrotina, o que permite atender muitos clientes ao mesmo tempo em uma única thread. Os clientes ativos ficam num dicionário `conexão → nome`.
- Cada mensagem recebida é retransmitida (broadcast) para todos os outros clientes, já com o nome do remetente. O envio é feito em paralelo com `asyncio.gather`, então um cliente lento não atrasa os demais.
- Entradas e saídas são avisadas a todos com mensagens do tipo `sistema`.
- O cliente Python roda duas tarefas em paralelo: uma recebe e exibe as mensagens, a outra lê o teclado (via `asyncio.to_thread`, para não travar o recebimento).

## Tratamento de erros

- **Desconexão inesperada** (aba fechada, `Ctrl+C` no cliente, queda de rede): a exceção `ConnectionClosed` é tratada, o cliente é removido no bloco `finally` e os demais recebem o aviso de saída — o servidor continua funcionando.
- Nome vazio, maior que 20 caracteres ou já em uso é recusado com uma mensagem de erro, e o usuário pode tentar outro.
- Mensagens vazias, JSON inválido ou com tipo desconhecido são ignorados.
- Mensagens são limitadas a 1000 caracteres.
- Servidor indisponível gera mensagem amigável nos dois clientes.
- No cliente HTML, o texto recebido é inserido com `textContent`, evitando injeção de HTML/JavaScript.

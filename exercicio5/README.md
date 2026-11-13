# Exercício 05 – Tráfego HTTP

**Objetivo:** Capturar e analisar requisições e respostas HTTP realizadas durante o acesso a um servidor web.

Foi capturado o tráfego gerado ao acessar o site `neverssl.com`, que utiliza HTTP sem criptografia. Com o filtro `http`, foram identificadas requisições com o método `GET` e respostas com os códigos `200 OK`, `301 Moved Permanently` e `204 No Content`. Na requisição analisada (pacote 640), a URL acessada foi `http://neverssl.com/`, e a resposta correspondente (pacote 645) retornou `200 OK` com Content-Type `text/html`.

## Evidências

* Captura geral dos pacotes HTTP e detalhamento da requisição (pacote 640):

![Pacote 640 – Requisição HTTP GET](Pacote%20640.png)

Arquivo de captura:  [`Exercicio-05-HTTP/captura-http.pcapng`](./Tráfego%20HTTP.pcapng)

## Integrantes do grupo

- Felipe Alcântara Guimarães Veloso
- Gabriel de Jesus Moraes Maurício
- Riquelme Moreira Campos

# Exercício 07 – Resolução de Nomes via DNS

**Objetivo:** Analisar o processo de resolução de nomes de domínio por meio do protocolo DNS.

Com o filtro `dns`, foram observadas consultas feitas pelo host `192.168.15.81` ao servidor DNS `192.168.15.1`. Para o domínio `csp.withgoogle.com`, houve uma consulta do tipo A, respondida com o IPv4 `172.217.172.49`, e uma do tipo AAAA, respondida com o IPv6 `2800:3f0:4001:844::2011`. Nesta captura não apareceram registros CNAME.

## Evidências

* Consultas DNS (tipos A e AAAA):

Pacote 84 – Consulta tipo A
![Pacote 84 – Consulta tipo A](Pacote%2084%20-%20Type%20A.png)

Pacote 85 – Consulta tipo AAAA
![Pacote 85 – Consulta tipo AAAA](Pacote%2085%20-%20Type%20AAAA.png)

* Respostas DNS:

Pacote 99 – Resposta tipo A
![Pacote 99 – Resposta tipo A](Pacote%2099%20-%20Type%20A%20(response).png)

Pacote 100 – Resposta tipo AAAA
![Pacote 100 – Resposta tipo AAAA](Pacote%20100%20-%20Type%20AAAA%20(response).png)

Arquivo de captura: [`Exercicio-07-DNS/captura-dns.pcapng`](./Resolução%20de%20Nomes%20via%20DNS.pcapng)

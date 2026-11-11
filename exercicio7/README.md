# Exercício 07 – Resolução de Nomes via DNS

**Objetivo:** Analisar o processo de resolução de nomes de domínio por meio do protocolo DNS.

Com o filtro `dns`, foram observadas consultas feitas pelo host `192.168.15.81` ao servidor DNS `192.168.15.1`. Para o domínio `csp.withgoogle.com`, houve uma consulta do tipo A, respondida com o IPv4 `172.217.172.49`, e uma do tipo AAAA, respondida com o IPv6 `2800:3f0:4001:844::2011`. Nesta captura não apareceram registros CNAME.

## Evidências

* Consultas DNS (tipos A e AAAA):

![Pacote 84 – Consulta tipo A](imagens/Pacote_84_-_Type_A.png)

![Pacote 85 – Consulta tipo AAAA](imagens/Pacote_85_-_Type_AAAA.png)

* Respostas DNS:

![Pacote 99 – Resposta tipo A](imagens/Pacote_99_-_Type_A__response_.png)

![Pacote 100 – Resposta tipo AAAA](imagens/Pacote_100_-_Type_AAAA__response_.png)

Arquivo de captura: `Exercicio-07-DNS/captura-dns.pcapng`

# Exercício 08 – Tráfego ICMP (Ping)

**Objetivo:** Analisar a comunicação ICMP e identificar o tempo de ida e volta dos pacotes (RTT).

O comando `ping` foi usado para testar a conectividade entre o computador (`192.168.15.81`) e outro dispositivo da rede local (`192.168.15.54`). Com o filtro `icmp`, foram identificados os pares Echo Request e Echo Reply. No primeiro par (pacotes 488 e 489), o RTT foi de 10,802 ms, valor exibido pelo Wireshark no campo `Response time`.

## Evidências

* Echo Request (pacote 488):

![Pacote 488 – Echo request](imagens/Pacote_488__request_.png)

* Echo Reply e tempo de resposta (pacote 489):

![Pacote 489 – Echo reply](imagens/Pacote_489__reply_.png)

Arquivo de captura: `Exercicio-08-ICMP/captura-icmp.pcapng`

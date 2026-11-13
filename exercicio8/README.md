# Exercício 08 – Tráfego ICMP (Ping)

**Objetivo:** Analisar a comunicação ICMP e identificar o tempo de ida e volta dos pacotes (RTT).

O comando `ping` foi usado para testar a conectividade entre o computador (`192.168.15.81`) e outro dispositivo da rede local (`192.168.15.54`). Com o filtro `icmp`, foram identificados os pares Echo Request e Echo Reply. No primeiro par (pacotes 488 e 489), o RTT foi de 10,802 ms, valor exibido pelo Wireshark no campo `Response time`.

O RTT dos demais pacotes foi calculado pela diferença entre o horário do Echo Reply e o do Echo Request correspondente (coluna Time): 
* Pacotes 501 e 503 = 110,700 ms;
* Pacotes 519 e 526 = 147,745 ms;
* Pacotes 545 e 547 = 176,289 ms;
* Pacotes 564 e 565 = 193,735 ms;
* Pacotes 582 e 583 = 114,088 ms.

## Evidências

* Echo Request (pacote 488):

Pacote 488 – Echo request
![Pacote 488 – Echo request](Pacote%20488%20(request).png)

* Echo Reply e tempo de resposta (pacote 489):

Pacote 489 – Echo reply
![Pacote 489 – Echo reply](Pacote%20489%20(reply).png)

Arquivo de captura: [`Exercicio-08-ICMP/captura-icmp.pcapng`](./Tráfego%20ICMP%20(ping).pcapng)

## Integrantes do grupo

- Felipe Alcântara Guimarães Veloso
- Gabriel de Jesus Moraes Maurício
- Riquelme Moreira Campos

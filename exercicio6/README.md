# Exercício 06 – Estabelecimento e Encerramento de Conexão TCP

**Objetivo:** Identificar o estabelecimento e o encerramento de uma conexão TCP.

Usando o Telnet na porta 80 de um servidor web, foi observado o Three-Way Handshake: `SYN` (pacote 43, retransmitido no 66), `SYN-ACK` (pacote 69) e `ACK` (pacote 71). O servidor respondeu com `400 Bad Request` e encerrou a conexão com a troca de `FIN, ACK` e `ACK` nos dois sentidos (pacotes 195, 196, 197 e 208).

## Evidências

* Estabelecimento da conexão (Three-Way Handshake):

Pacote 43 – SYN
![Pacote 43 – SYN](Estabelecimento%20de%20Conexão%20-%20Pacote%2043%20(SYN).png)

Pacote 69 – SYN-ACK
![Pacote 69 – SYN-ACK](Estabelecimento%20de%20Conexão%20-%20Pacote%2069%20(SYN-ACK).png)

Pacote 71 – ACK
![Pacote 71 – ACK](Estabelecimento%20de%20Conexão%20-%20Pacote%2071%20(ACK).png)

* Encerramento da conexão:

Pacote 195 – FIN-ACK
![Pacote 195 – FIN-ACK](Encerramento%20de%20Conexão%20-%20Pacote%20195%20(FIN-ACK).png)

Pacote 196 – ACK
![Pacote 196 – ACK](Encerramento%20de%20Conexão%20-%20Pacote%20196%20(ACK).png)

Pacote 197 – FIN-ACK
![Pacote 197 – FIN-ACK](Encerramento%20de%20Conexão%20-%20Pacote%20197%20(FIN-ACK).png)

Pacote 208 – ACK
![Pacote 208 – ACK](Encerramento%20de%20Conexão%20-%20Pacote%20208%20(ACK).png)

Arquivo de captura:  [`Exercicio-06-TCP/captura-tcp.pcapng`](./Estabelecimento%20e%20Encerramento%20de%20Conexão%20TCP.pcapng)

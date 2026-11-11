# Exercício 06 – Estabelecimento e Encerramento de Conexão TCP

**Objetivo:** Identificar o estabelecimento e o encerramento de uma conexão TCP.

Usando o Telnet na porta 80 de um servidor web, foi observado o Three-Way Handshake: `SYN` (pacote 43, retransmitido no 66), `SYN-ACK` (pacote 69) e `ACK` (pacote 71). O servidor respondeu com `400 Bad Request` e encerrou a conexão com a troca de `FIN, ACK` e `ACK` nos dois sentidos (pacotes 195, 196, 197 e 208).

## Evidências

* Estabelecimento da conexão (Three-Way Handshake):

![Pacote 43 – SYN](imagens/Estabelecimento_de_Conexão_-_Pacote_43__SYN_.png)

![Pacote 69 – SYN-ACK](imagens/Estabelecimento_de_Conexão_-_Pacote_69__SYN-ACK_.png)

![Pacote 71 – ACK](imagens/Estabelecimento_de_Conexão_-_Pacote_71__ACK_.png)

* Encerramento da conexão:

![Pacote 195 – FIN-ACK](imagens/Encerramento_de_Conexão_-_Pacote_195__FIN-ACK_.png)

![Pacote 196 – ACK](imagens/Encerramento_de_Conexão_-_Pacote_196__ACK_.png)

![Pacote 197 – FIN-ACK](imagens/Encerramento_de_Conexão_-_Pacote_197__FIN-ACK_.png)

![Pacote 208 – ACK](imagens/Encerramento_de_Conexão_-_Pacote_208__ACK_.png)

Arquivo de captura: `Exercicio-06-TCP/captura-tcp.pcapng`

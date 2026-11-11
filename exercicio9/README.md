# Exercício 09 – Tráfego DHCP

**Objetivo:** Identificar o processo de atribuição automática de endereços IP por meio do protocolo DHCP.

Foi gerada uma nova negociação DHCP, precedida por um `DHCP Release` (pacote 420) em que o cliente liberou o endereço anterior. Com o filtro `dhcp`, foram identificadas as quatro etapas do processo DORA: Discover (558), Offer (559), Request (560) e ACK (565), todas com o mesmo Transaction ID `0x5c8de302`. O servidor DHCP `192.168.15.1` ofereceu e confirmou o endereço `192.168.15.81` para o cliente.

## Evidências

* DHCP Release (pacote 420):

![Pacote 420 – Release](imagens/Pacote_420_-_Release.png)

* DHCP Discover (pacote 558):

![Pacote 558 – Discover](imagens/Pacote_558_-_Discover.png)

* DHCP Offer (pacote 559):

![Pacote 559 – Offer](imagens/Pacote_559_-_Offer.png)

* DHCP Request (pacote 560):

![Pacote 560 – Request](imagens/Pacote_560_-_Request.png)

* DHCP ACK (pacote 565):

![Pacote 565 – ACK](imagens/Pacote_565_-_ACK.png)

Arquivo de captura: `Exercicio-09-DHCP/captura-dhcp.pcapng`

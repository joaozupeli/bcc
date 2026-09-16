# Folha AS01 — versão curta (1 folha frente/verso)
Nome + turma no topo. Letra pequena.

---

# FRENTE

**OSI ↑:** Aplicação(7 HTTP/DNS/FTP/SMTP) · Apresentação(6 TLS/JPEG) · Sessão(5 Zoom) · Transporte(4 TCP/UDP, porta) · Rede(3 IP, ROTEADOR) · Enlace(2 quadro/MAC, SWITCH) · Física(1 bits, HUB)

**TCP/IP:** Aplicação(7+6+5, mensagem) · Transporte(segmento TCP / datagrama UDP) · Internet(pacote IP) · Acesso à rede(quadro)

**Encapsula:** app → TCP/UDP → IP → Ethernet → bits. Destino desencapsula. `'A'`=65=`01000001`

Pilha: `HTTP+TCP+IP+Ethernet`. Mesma camada = não juntos (TCP **ou** UDP).

**PDU** = cabeçalho+dados. Ethernet: Preâm(7)+Del(1)+MAC dest(6)+orig(6)+Tipo(2)+Dados(46–1500)+CRC(4)
Tipo: `0800` IPv4 · `0806` ARP · `86DD` IPv6
**MAC** 48 bits, só LAN. 3B fabricante + 3B aparelho. Dá p/ mudar (`ip link`).

PAN Bluetooth · **LAN** Ethernet/Wi-Fi 802.3/802.11 · MAN cidade · **WAN** roteador
Unicast 1-1 · Broadcast todos · Multicast grupo (`224–239.x`)
Topo: ponto a ponto, barramento, **estrela**, anel, árvore, mesh

| | HUB L1 | SWITCH L2 |
|---|---|---|
| Faz | grita p/ todos | entrega pelo **MAC** |
| Tabela | não | MAC↔porta (só o que viu) |

Cascata: hub = todos do hub veem. Switch da ponta **não lista todos** os MACs (só o que passou na porta dele / uplink).

`ip a` meu IP · `ip route` gateway · `ping` ICMP (GW=LAN; 8.8.8.8=Internet) · `traceroute` saltos (1º=GW) · `nslookup` DNS · `arp -a` IP→MAC · `ss -tuln` portas
Interface down → ping morre. Rotas da Internet **mudam**.

PT: Simulation vê PDU. PC: IP+máscara+GW. Switch `show mac-address-table`. Roteador `show ip route`.

---

# VERSO

**IPv4** 32 bits. Máscara: 1=rede 0=host. `/24`=`255.255.255.0`
```
h=32−prefixo    hosts=2^h−2    bloco=2^h
rede=IP AND másc    broadcast=rede+bloco−1
1º=rede+1    último=broadcast−1
bloco no octeto=256−nº da máscara
```
Mesma LAN = mesma rede. Host 000...=rede. Host 111...=broadcast.

| / | másc | hosts | bloco |
|---|---|---|---|
| 8 | 255.0.0.0 | 16M | — |
| 16 | 255.255.0.0 | 65k | — |
| 20 | 255.255.240.0 | 4094 | 16 (3º) |
| 24 | 255.255.255.0 | 254 | 256 |
| 25 | .128 | 126 | 128 |
| 26 | .192 | 62 | 64 |
| 27 | .224 | 30 | 32 |
| 28 | .240 | 14 | 16 |
| 29 | .248 | 6 | 8 |
| 30 | .252 | **2** | 4 |

Classe A 1–126 /8 · B 128–191 /16 · C 192–223 /24 · D 224–239 multi · E 240+
Privado: `10/8` `172.16/12` `192.168/16` · Loop `127/8` · APIPA `169.254/16`
GW = roteador da LAN (quase sempre `.1`). NAT = muitos privados → 1 público.
4 sub-redes iguais: +2 bits (`/24`→`/26`).

**Conta pronta:** `192.168.2.100/26` → bloco 64 → rede **.64** · 1º **.65** · último **.126** · broad **.127** · 62 hosts
`192.168.2.100` + `255.255.240.0`=/20 → rede **192.168.0.0** · broad **.15.255** · 4094 hosts

**ICMP**=ping · **ARP**=IP→MAC (outra rede? ARP do **GW**, não do destino) · **IGMP**=multicast
IP hdr: TTL (morre em 0) · Proto **1 ICMP / 6 TCP / 17 UDP**
Intra-LAN: MAC=PC dest. Inter-rede: MAC=**roteador**. **IP não muda. MAC muda a cada salto.**

Roteador L3: lê dest → tabela → next-hop.
Tabela: rede+másc | GW | iface | custo. Sem GW=ligada. `0.0.0.0/0`=default. Maior prefixo ganha.
Estático=mão · Dinâmico=OSPF/RIP/BGP sozinho
Vetor dist (saltos) RIP · Estado enlace OSPF · Vetor caminho **BGP** (entre AS)
AS=rede de uma org (ASN). IGP interno · BGP externo.

```
PC1 192.168.10.10/24 GW .1 | R1 .1 e 10.0.12.1/30
R2 10.0.12.2/30 e 192.168.20.1/24 | PC2 .20 GW .1
R1: 192.168.20.0/24 via 10.0.12.2
R2: 192.168.10.0/24 via 10.0.12.1
```

**Porta** acha o programa. Soquete=`IP:porta`  0–1023 conhecidas · 1024–49151 regist. · 49152–65535 efêmeras
Mux=junta · Demux=entrega na porta dest.

| | TCP | UDP |
|---|---|---|
| conexão | sim SYN/SYN-ACK/ACK | não |
| confiável/ordem/fluxo | sim | não |
| hdr | 20 B | 8 B |
| uso | HTTP FTP SMTP SSH | DNS DHCP VoIP jogo |

Fecha FIN · aborta RST · NS=1º byte · ACK=próximo esperado
**MTU 1500 · MSS=1500−40=1460** (opção no SYN)

20/21 FTP · 22 SSH · 23 Telnet · 25 SMTP · 53 DNS · 67/68 DHCP · 80 HTTP · 110 POP3 · 143 IMAP · 443 HTTPS · 3389 RDP

Ping GW ok + 8.8.8.8 falha = Internet/rota. Nome falha + IP pinga = DNS. Precisa chegar inteiro = TCP. Precisa rápido = UDP.

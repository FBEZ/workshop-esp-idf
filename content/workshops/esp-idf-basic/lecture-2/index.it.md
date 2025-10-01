---
title: "ESP-IDF Base - Lezione 2"
date: "2025-11-12"
series: ["WS00A"]
series_order: 4
showAuthor: false
summary: "In questa lezione introduciamo la struttura a strati della comunicazione internet, spiegando il modello ISO/OSI e il processo di incapsulamento dei dati. Approfondiamo inoltre i protocolli HTTP e MQTT, mostrando come le REST API e il formato JSON consentano la comunicazione tra dispositivi."
---

## Connettività Internet

Le applicazioni comunicano su internet utilizzando diversi protocolli che si basano l'uno sull'altro, formando una struttura a strati chiamati "layer".

Il **modello ISO/OSI** è un quadro *concettuale* che suddivide in sette strati il modo in cui i dati (come messaggi, video o pagine web) viaggiano attraverso le reti.
Ogni strato ha una propria funzione e utilizza specifici **protocolli**.

Il modello ISO/OSI solito viene rappresentato come in Fig.1.

{{< figure
default=true
src="/workshops/esp-idf-basic/assets/lec_2_isoosi.webp"
height=500
caption="Fig.1 - Stack ISO/OSI"

>}}

Partendo dal basso, gli strati sono:

1. **Fisico (PHY)** – Specifica come deve interagire l'hardware dei due dispositivi che comunicano tra loro: segnali di tensione, radio, antenne e frequenze.<br>
   *Esempio: Wi-Fi, Ethernet*

2. **Collegamento Dati (Data Link)** – Gestisce la connessione diretta tra dispositivi (come laptop e router) e l’accesso al canale wireless.<br>
   *Esempio: MAC (Media Access Control)*

3. **Rete (Network)** – Si occupa di come i dati passano da una rete all’altra.<br>
   *Esempio: IP (Internet Protocol)*

4. **Trasporto (Transport)** – Garantisce che i dati vengano consegnati correttamente e nell’ordine giusto.<br>
   *Esempi: TCP (Transmission Control Protocol), UDP (User Datagram Protocol)*

5. **Sessione (Session)** – Gestisce e mantiene le connessioni tra dispositivi o applicazioni.<br>
   *Esempi: TLS, NetBIOS, SMB*

6. **Presentazione (Presentation)** – Traduce i dati in modo che siano leggibili da entrambe le parti (ad esempio decifrando un messaggio criptato).<br>
   *Esempi: SSL/TLS, JPEG, MP3, ASCII*

7. **Applicazione (Application)** – È ciò che vede l’utente: siti web, videochiamate, email, ecc.<br>
   *Esempi: HTTP, SMTP, FTP, DNS*

Alcuni protocolli gestiscono più strati contemporaneamente. Ad esempio, il protocollo Ethernet si occupa sia dello strato fisico che di quello di collegamento dati.

Ogni strato passa il proprio risultato al successivo.
Diversi protocolli ad alto livello, possono riutilizzare gli stessi strati inferiori: ad esempio, **MQTT** si trova allo stesso livello di HTTP, e entrambi utilizzano lo stack TCP/IP.

### Incapsulamento

La combinazione dei livelli avviene tramite **incapsulamento**.

L’incapsulamento è il processo con cui il payload di un protocollo a basso livello racchiude l'intero frame dei protocolli superiori. 
Nel contesto di una rete Wi-Fi, i dati dell’applicazione vengono prima incapsulati in un **segmento TCP**, poi in un **pacchetto IP** e infine in un **frame Wi-Fi (IEEE 802.11)** o **Ethernet**.
Ogni strato aggiunge il proprio *header* (e talvolta un *trailer*) per consentire una comunicazione modulare ed efficiente.

Un’immagine vale più di mille parole:

{{< figure
default=true
src="/workshops/esp-idf-basic/assets/lec_2_encapsulation.webp"
height=500
caption="Fig.2 - Incapsulamento"

>}}

In breve, tutto il contenuto del livello superiore è incluso nel campo *payload* (o *data*) del protocollo di livello inferiore.

## Connettività nei dispositivi Espressif

Ora che abbiamo compreso i livelli di connettività, vediamo quale tipo di connettività è supportato dai moduli Espressif.

### Strati fisici

I moduli Espressif supportano tre principali PHY, a seconda del SoC:

1. **Wi-Fi** – Supportato da tutti i dispositivi (ad eccezione della famiglia H); consente la connessione a un router e quindi a internet. Sarà il focus di questo workshop.
2. **BLE** – Usato principalmente per la comunicazione diretta con uno smartphone e per il provisioning (configurazione iniziale).
3. **Thread/Zigbee** – Protocolli IoT utilizzati per comunicazioni **locali** macchina-a-macchina (M2M) basate su topologia mesh (molti-a-molti). Per connettersi a Internet serve un bridge Thread–Wi-Fi.

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
Il protocollo Matter utilizza tutti questi livelli di connettività: BLE per il provisioning, Thread per la comunicazione a basso consumo e Wi-Fi per il trasferimento di dati ad alta velocità.
{{< /alert >}}

In questo workshop ci concentreremo solo sul Wi-Fi.
Vediamo brevemente la sua topologia.

#### Topologia Wi-Fi

In una rete Wi-Fi ci sono due ruoli principali: **Access Point (AP)** e **Station (STA)**.

* L’**Access Point (AP)** è il dispositivo centrale (come un router) che trasmette la rete wireless e connette le stazioni tra loro e con reti esterne come internet.
* Una **Station (STA)** è qualsiasi dispositivo che si collega all’AP: smartphone, laptop o dispositivo IoT.

L’AP gestisce il mezzo wireless, mentre le STA comunicano **attraverso** l’AP, mai direttamente tra loro.

{{< figure
default=true
src="/workshops/esp-idf-basic/assets/lec_2_sta_ap.webp"
height=500
caption="Fig.3 - STA and AP"

>}}

{{< alert icon="circle-info" cardColor="#b3e0f2" iconColor="#04a5e5">}}
I moduli Espressif possono funzionare in entrambe le modalità.
{{< /alert >}}

Per connettersi a un AP, una stazione ha bisogno di due dati:
* L'**SSID**, ossia il nome della rete
* La **password** del AP.

Nella prima parte dell’esercitazione, imposteremo il dispositivo Espressif in modalità AP e useremo lo smartphone per controllare la connessione.

### Protocolli di livello applicativo

Nel mondo IoT, esistono diversi protocolli di comunicazione, tra cui i più comuni sono MQTT e HTTP.

**MQTT** è progettato per la comunicazione **macchina-a-macchina (M2M)** ed è ampiamente usato per reti di sensori e attuatori, specialmente in domotica.

**HTTP** è il protocollo alla base del web, utilizzato principalmente per fornire contenuti HTML. Un’altra applicazione importante dell'HTTP nell’IoT è l’implementazione di **REST API**, che permettono l’interazione tra dispositivi tramite richieste HTTP.

Ad esempio, un’applicazione web per la casa intelligente può mostrare lo stato di vari sensori interrogando una **REST API** esposta da un **gateway di sensori**, che funge da ponte tra i dispositivi e l’interfaccia utente.

In questo workshop useremo HTTP per servire una semplice pagina HTML e per implementare una REST API.

## HTTP, HTML e JSON: Servire pagine web e creare REST API

HTTP può essere utilizzato sia per servire pagine HTML (visualizzate nei browser) che dati strutturati come JSON (per interfaccia verso altri software).

### Le basi dell'HTTP

**HTTP (Hypertext Transfer Protocol)** è il fondamento della comunicazione web, basato su un semplice modello **client-server**.
Il client (browser o app) invia una richiesta al server, che la elabora e restituisce una risposta.

#### Richieste HTTP

HTTP definisce diversi metodi di richiesta, ciascuno con uno scopo specifico:

* **GET** – Recupera dati dal server
* **POST** – Invia o crea nuovi dati sul server
* **PUT/PATCH** – Aggiorna dati esistenti
* **DELETE** – Elimina dati

#### Risposte HTTP

Dopo aver ricevuto una richiesta, il server risponde con un codice di stato che indica il risultato:

* **200 OK** – Richiesta eseguita con successo
* **201 Created** – Nuova risorsa creata (tipicamente dopo una POST)
* **400 Bad Request** – Sintassi della richiesta non valida
* **401 Unauthorized** – Autenticazione richiesta o fallita
* **404 Not Found** – Risorsa non trovata
* **500 Internal Server Error** – Errore generico sul server

Le applicazioni moderne e i sistemi IoT utilizzano spesso **JSON (JavaScript Object Notation)** per scambiare dati strutturati. Questo è anche il formato alla base delle API REST.

{{< figure
default=true
src="/workshops/esp-idf-basic/assets/lec_2_http_request.webp"
height=500
caption="Fig.4 - Interazione client-server"

>}}

### HTML: pagine web

**HTML (HyperText Markup Language)** è il linguaggio standard per creare pagine web.
Con ESP-IDF, è possibile servire pagine HTML direttamente dal dispositivo embedded tramite protocollo HTTP.

Le pagine HTML possono essere usate per:

* Visualizzare letture di sensori in tempo reale
* Fornire interfacce di controllo (pulsanti, slider, ecc.)
* Permettere la configurazione della rete o dei parametri

Un semplice esempio di pagina HTML servita da un dispositivo Espressif è il seguente. 

```html
<!DOCTYPE html>
<html>
<head>
  <title>Dashboard Sensore Espressif</title>
</head>
<body>
  <h1>Sensore Salotto</h1>
  <p>Temperatura: 22.5°C</p>
  <p>Umidità: 60%</p>
</body>
</html>
```

In Fig.5 puoi vedere il rendering della pagina HTML. 

{{< figure
default=true
src="/workshops/esp-idf-basic/assets/lec_2_html_rendering.webp"
height=300
caption="Fig.5 - Rendering della pagina HTML"
    >}}


Servire contenuti HTML dal dispositivo permette agli utenti di interagire con esso tramite un browser, senza software aggiuntivo.

### JSON: REST API

**JSON** è un formato leggero e leggibile per rappresentare dati strutturati, ideale per applicazioni web e IoT.
Un oggetto JSON è composto da coppie chiave-valore, ad esempio:

```json
{
  "temperature": 22.5,
  "humidity": 60,
  "sensor": "living_room"
}
```

#### REST API

Una **REST API** (Representational State Transfer) permette alle applicazioni di interagire con un server usando i metodi HTTP standard.
Le risorse sono accessibili tramite **route** (percorsi URL) strutturate e leggibili.

**Esempi di route API REST**:

* `GET /sensors` – Elenca tutti i sensori
* `GET /sensors/42` – Mostra i dati del sensore 42
* `POST /sensors` – Crea un nuovo sensore
* `PUT /sensors/42` – Aggiorna le impostazioni del sensore 42
* `DELETE /sensors/42` – Elimina il sensore 42

Nel secondo modulo del workshop, implementerai una semplice pagina HTML e una REST API utilizzando HTTP.

## Conclusione

In questa lezione abbiamo introdotto la struttura a livelli della comunicazione Internet, il modello ISO/OSI, l’incapsulamento dei dati e l’uso di protocolli come HTTP e MQTT.
Abbiamo inoltre visto come le REST API e il formato JSON permettano una comunicazione strutturata tra dispositivi e applicazioni — fondamenta dei moderni sistemi IoT connessi.

Ora hai tutte le basi teoriche per iniziare gli esercizi di questa sezione. 

### Prossimo passo

> Prossimo esercizio → **[Esercizio 2.1](../assignment-2-1/)**

> Oppure [torna al menù di navigazione](../#agenda)
